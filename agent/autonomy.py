"""V5.5 - cycle autonome borne : demarrer, choisir, chercher, filtrer, sauvegarder, memoriser, preparer la suite.

    python -m agent.run cycle            un cycle (planificateur Windows, GitHub Actions ou a la main)
    python -m agent.run queue            etat de la file et prochaines recherches

Garde-fous (config/autonomy.json) : verrou anti double lancement, budget de temps par cycle,
nombre d'elements par cycle et par jour, lectures par jour, profondeur des relances, taille de la file.
Le cycle n'utilise aucun service payant ni aucun modele d'IA ; il ne modifie jamais le code de l'agent
et ne reecrit pas les fiches existantes (il cree des fiches ou ajoute une requete a leur en-tete, comme V5.4).
"""
from __future__ import annotations

import json
import os
import time
import traceback
import uuid
from pathlib import Path

from agent import knowledge, meta, rag
from agent import budget as limits
from agent.evaluation import evaluate_library, evaluate_note
from agent.planner import short
from agent.followup_rules import followups_for_note, missing_info
from agent.recursive_gaps import propose
from agent.research_queue import ResearchQueue, iso, load_config, now_ts, today

ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------- verrou
class Busy(RuntimeError):
    pass


class Lock:
    """Fichier output/vdn.lock cree de facon exclusive. Un verrou plus vieux que stale_after_s est repris."""

    def __init__(self, root: Path, stale_after_s: int):
        self.path = Path(root) / "output" / "vdn.lock"
        self.stale = stale_after_s
        self.took_over = False
        self.owner = uuid.uuid4().hex

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Stable advisory guard serializes stale-file takeover, including two
        # contenders inspecting the same expired JSON. OS releases it on crash.
        self.guard = (self.path.parent / 'vdn.guard').open('a+b')
        try:
            if os.name == 'nt':
                import msvcrt
                if self.guard.seek(0, os.SEEK_END) == 0:
                    self.guard.write(b'0')
                    self.guard.flush()
                self.guard.seek(0)
                msvcrt.locking(self.guard.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.guard.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            self.guard.close()
            raise Busy('un cycle est deja en cours (verrou systeme)') from e
        try:
            return self._enter_file()
        except BaseException:
            self.guard.close()
            raise

    def _enter_file(self):
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump({"pid": os.getpid(), "started": iso(), "ts": now_ts(), 'owner': self.owner}, f)
                return self
            except FileExistsError:
                try:
                    info = json.loads(self.path.read_text(encoding="utf-8"))
                    if not isinstance(info, dict) or not isinstance(info.get('ts'), (int, float)):
                        raise ValueError('incomplete lock metadata')
                except (ValueError, OSError):
                    # A new exclusive file may still be receiving its JSON.
                    try:
                        info = {"ts": self.path.stat().st_mtime}
                    except FileNotFoundError:
                        continue
                if now_ts() - float(info.get("ts", 0)) <= self.stale:
                    raise Busy(f"un cycle est deja en cours (depuis {info.get('started', '?')})")
                self.path.unlink(missing_ok=True)
                self.took_over = True
        raise Busy("verrou impossible a obtenir")

    def __exit__(self, *exc):
        try:
            info = json.loads(self.path.read_text(encoding='utf-8'))
            if info.get('owner') == self.owner:
                self.path.unlink(missing_ok=True)
        except (OSError, ValueError):
            pass
        finally:
            self.guard.close()
        return False


# ---------------------------------------------------------------------------- journaux
def log_error(root: Path, where: str, err: BaseException | str):
    p = Path(root) / "output" / "errors.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    detail = err if isinstance(err, str) else f"{type(err).__name__}: {err}"
    tb = "" if isinstance(err, str) else traceback.format_exc(limit=4)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"utc": iso(), "where": where, "error": str(detail)[:500], "trace": tb[-1500:]}, ensure_ascii=False) + "\n")


def write_daily_report(root: Path, summary: dict) -> Path:
    """Ajoute la section de ce cycle au rapport du jour (output/reports/AAAA-MM-JJ.md). Ne remplace rien."""
    folder = Path(root) / "output" / "reports"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{today()}.md"
    lines = []
    if not path.exists():
        lines += [f"# Rapport VDN du {today()}", "",
                  "Les fiches sont des pistes **non testées dans Roblox Studio** tant que `tested_in_studio` n'est pas coché à la main.", ""]
    s = summary
    lines += [f"## Cycle {s['started']} → {s['finished']} ({s['stop_reason']})", "",
              f"- Recherches traitées : {len(s['items'])} · fiches créées : {s['created']} · lues : {s['fetched']} · "
              f"rejetées : {s['rejected']} · erreurs : {len(s['errors'])}",
              f"- Relances ajoutées : {s['followups_added']} · file : {s['queue']['counts']['pending']} en attente, "
              f"{s['queue']['counts']['done']} faites · aujourd'hui : {s['queue']['daily']['items']} recherches", ""]
    for it in s["items"]:
        lines.append(f"### « {it['query']} » ({it['topic']}, profondeur {it['depth']}, {it['origin']})")
        lines.append(f"- Résultat : {it['status']} · créées {it.get('created', 0)} · rejetées {it.get('rejected', 0)} · "
                     f"doublons {it.get('duplicates', 0)}")
        for n in it.get("notes", []):
            gaps = "; ".join(n["missing"]) or "aucune lacune repérée automatiquement"
            lines.append(f"  - [[{Path(n['path']).stem}]] — statut {n['status']} — lacunes : {gaps}")
        for f in it.get("followups", []):
            lines.append(f"  - relance : « {f['query']} » → {f.get('topic', it['topic'])} — {f['reason']}")
        if it.get("error"):
            lines.append(f"- Erreur : {it['error']}")
        lines.append("")
    if s["queue"]["next"]:
        lines += ["**Prochaines recherches :** " + " · ".join(f"« {n['query']} »" for n in s["queue"]["next"]), ""]
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return path


def schedule_gaps(q: ResearchQueue, report: dict) -> int:
    """Revisit old shallow notes too; bounded, lexical, and never alters a note."""
    added = 0
    facets = {'source_traceability': 'evidence', 'actionable_steps': 'tutorial', 'parameters': 'settings',
              'constraints': 'constraints', 'prerequisites': 'prerequisites',
              'alternatives': 'alternatives', 'reproducibility': 'reproduction'}
    for note in report['notes']:
        if note.get('topic') not in q.topics or note.get('claimed_status') not in ('candidat', 'documente'):
            continue
        queries = note.get('queries', [])
        if not queries or not isinstance(queries[0], str):
            continue
        ancestor = next((it for it in q.data['items'].values() if it['query'] in queries), None)
        depth = ancestor['depth'] + 1 if ancestor else 0
        note_added = 0
        for gap in note['gaps']:
            if added >= q.cfg['queue']['max_children_per_item']:
                return added
            if note_added >= q.cfg['queue']['max_children_per_note']:
                break
            query = f"{short(queries[0], 3)} {facets[gap]}"
            ok, why = q.add(note['topic'], query, q.topics[note['topic']].get('priority', 5) - .5,
                           origin='reevaluation', depth=depth, parent=ancestor['key'] if ancestor else None,
                           reason=f"fiche {note.get('id')} : {gap} absent", research_signals={'gap_importance': len(note['gaps'])})
            if ok:
                added += 1
                note_added += 1
    return added


# ---------------------------------------------------------------------------- cycle
def cycle(root: Path = ROOT, provs=None, max_items: int | None = None, time_budget_s: float | None = None,
          research_fn=None) -> dict:
    """Un cycle autonome complet. ``provs`` et ``research_fn`` permettent les tests hors ligne."""
    root = Path(root)
    cfg = load_config(root)
    if research_fn is None:
        from agent.run import research as research_fn
    c = cfg["cycle"]
    max_items = max(0, min(int(max_items if max_items is not None else c["max_items"]), c['max_items']))
    budget = min(float(time_budget_s if time_budget_s is not None else c["time_budget_s"]), c['time_budget_s'])
    t0 = now_ts()
    monotonic_start = time.monotonic()
    summary = {"schema": "vdn.cycle/1", "started": iso(t0), "finished": None, "stop_reason": "", "items": [],
               "created": 0, "fetched": 0, "rejected": 0, "followups_added": 0, "seeded": 0, "recovered": 0,
               "errors": [], "lock_taken_over": False}
    try:
        with Lock(root, cfg["lock"]["stale_after_s"]) as lock:
            summary["lock_taken_over"] = lock.took_over
            q = ResearchQueue(root, cfg)
            summary["recovered"] = q.recovered
            if q.pending_count() == 0:
                summary["seeded"] = q.seed_from_topics()
            q.save()
            evaluation = evaluate_library(root)
            meta.save_json(root / 'output' / 'knowledge_evaluation.json', evaluation)
            summary['reevaluations_added'] = schedule_gaps(q, evaluation)
            q.save()
            daily = q.daily()
            def checkpoint(resource):
                cap = cfg['daily']['max_http_calls'] if resource == 'http_calls' else cfg['daily']['max_fetch']
                if daily[resource] >= cap:
                    raise limits.BudgetExhausted('quota quotidien HTTP atteint' if resource == 'http_calls' else 'quota de lectures atteint')
                daily[resource] += 1
                q.save()
            guard = limits.Budget(budget - (time.monotonic() - monotonic_start),
                                  min(c['max_http_calls'], max(0, cfg['daily']['max_http_calls'] - daily['http_calls'])), checkpoint)
            room = min(max_items, max(0, cfg["daily"]["max_items"] - daily["items"]))
            batch = q.next_batch(room)
            if not batch:
                summary["stop_reason"] = "quota quotidien atteint" if room == 0 else "file vide"
            attempted, used_topics = set(), set()
            for _ in range(room):
                # Re-rank after every observation; don't retry the same item in a cycle.
                batch = [it for it in q.next_batch(cfg['queue']['max_size']) if it['key'] not in attempted]
                if not batch:
                    summary['stop_reason'] = 'prerequis non resolus' if q.pending_count() else 'file vide'
                    break
                it = next((it for it in batch if it['topic'] not in used_topics), batch[0])
                attempted.add(it['key'])
                used_topics.add(it['topic'])
                try:
                    guard.check()
                except limits.BudgetExhausted as e:
                    summary['stop_reason'] = str(e)
                    break
                if daily["fetch"] >= cfg["daily"]["max_fetch"]:
                    summary["stop_reason"] = "quota de lectures atteint"
                    break
                with limits.using(guard):
                    summary["items"].append(_run_item(root, q, it, cfg, provs, research_fn, summary))
                meta.save_json(root / 'output' / 'knowledge_evaluation.json', evaluate_library(root))
                q.save()
                if summary['items'][-1].get('stop_reason'):
                    summary['stop_reason'] = summary['items'][-1]['stop_reason']
                    break
            summary['http_calls'] = guard.http_calls
            summary["stop_reason"] = summary["stop_reason"] or "cycle termine"
            try:
                (root / "knowledge").mkdir(parents=True, exist_ok=True)
                knowledge.build_indexes(root)
                rag.update_index(root)
            except Exception as e:  # l'index se reconstruira au cycle suivant
                log_error(root, "index", e)
                summary["errors"].append(f"index : {type(e).__name__}: {e}")
            summary["queue"] = q.summary()
            summary["finished"] = iso()
            summary["report"] = str(write_daily_report(root, summary).relative_to(root)).replace('\\', '/')
            meta.save_json(root / 'output' / 'last_cycle.json', summary)
    except Busy as e:
        summary["stop_reason"] = str(e)
        summary["queue"] = ResearchQueue(root, cfg, recover=False).summary() if (root / "output" / "queue.json").exists() else \
            {"counts": {"pending": 0, "done": 0}, "daily": {"items": 0}, "next": []}
        summary["finished"] = iso()
        return summary
    return summary


def _run_item(root: Path, q: ResearchQueue, it: dict, cfg: dict, provs, research_fn, summary: dict) -> dict:
    topic = q.topics[it["topic"]]
    c = cfg["cycle"]
    out = {"query": it["query"], "topic": it["topic"], "depth": it["depth"], "origin": it["origin"], "status": "done"}
    q.daily()['items'] += 1  # durable before network, including interrupted attempts
    q.mark_running(it)
    fetch_before = q.daily()['fetch']
    http_before = q.daily()['http_calls']
    try:
        st = research_fn(root, max_queries=1, per_source=c["per_source"], max_fetch=min(c["max_fetch_per_item"], cfg['daily']['max_fetch'] - fetch_before),
                         pause=c["pause_s"], provs=provs, planned=[(topic, it["query"], it["origin"])], finalize=False,
                         touch_existing=False)
    except Exception as e:
        log_error(root, f"recherche « {it['query']} »", e)
        q.mark_failed(it, f"{type(e).__name__}: {e}")
        summary["errors"].append(f"{it['query']} : {type(e).__name__}: {e}")
        return {**out, "status": "echec", "error": f"{type(e).__name__}: {e}"}
    for err in st.get("errors", []):
        log_error(root, f"source « {it['query']} »", str(err))
    summary["errors"] += st.get("errors", [])
    # Injected providers may not use the HTTP context; account for their reports.
    q.daily()["fetch"] += max(0, st.get('fetch_attempts', st.get('fetched', 0)) - (q.daily()['fetch'] - fetch_before))
    summary["fetched"] += st.get("fetched", 0)
    summary["created"] += st.get("created", 0)
    summary["rejected"] += st.get("rejected", 0)
    notes, follow = [], []
    for n in st.get("created_notes", []) + st.get('known_notes', []):
        path = root / n["path"]
        body = path.read_text(encoding="utf-8") if path.exists() else ""
        evaluation = evaluate_note(body)
        notes.append({**n, "missing": missing_info(body), 'evaluation': evaluation})
        if not path.exists() or it["depth"] >= cfg["queue"]["max_depth"]:
            continue
        note_added = 0
        for f in followups_for_note(path, it["query"], cfg["queue"]["max_children_per_note"]):
            target = q.best_topic(f["query"], it["topic"])
            ok, why = q.add(target, f["query"], priority=it["priority"] - 0.5, origin="relance",
                            depth=it["depth"] + 1, parent=it["key"], reason=f["reason"])
            if ok:
                follow.append({**f, "topic": target})
                summary["followups_added"] += 1
                note_added += 1
        for gap, facet in (('prerequisites', 'prerequisites'), ('alternatives', 'alternatives'), ('reproducibility', 'reproduction')):
            if note_added >= cfg['queue']['max_children_per_note']:
                break
            if gap not in evaluation['gaps']:
                continue
            f = {'query': f"{short(it['query'], 3)} {facet}", 'reason': f"diagnostic {n['id']} : {gap} absent"}
            ok, why = q.add(q.best_topic(f['query'], it['topic']), f['query'], priority=it['priority'] - .5,
                           origin='relance', depth=it['depth'] + 1, parent=it['key'], reason=f['reason'],
                           research_signals={'gap_importance': len(evaluation['gaps']),
                                             'source_quality': 1 / max(1, evaluation.get('source_tier') or 4)})
            if ok:
                follow.append(f)
                summary['followups_added'] += 1
                note_added += 1
    # V6 : les sources pertinentes mais insuffisantes peuvent declencher une recherche
    # plus precise, meme si aucune fiche n'a ete creee. Aucune fiche faible n'est publiee.
    # A barren branch stops after a configurable number of consecutive searches.
    progress = bool(st.get('created_notes'))
    stagnation = 0 if progress else 1
    ancestor = q.data['items'].get(it.get('parent'))
    if not progress and ancestor:
        stagnation += (ancestor.get('result') or {}).get('stagnation', 0)
    can_expand = not st.get('stop_reason') and not st.get('errors') and stagnation < cfg['queue']['stagnation_limit']
    if it["depth"] < cfg["queue"]["max_depth"] and can_expand:
        for f in propose(it["query"], st.get("rejected_candidates", []),
                         cfg["queue"].get("max_children_per_note", 3)):
            target = q.best_topic(f["query"], it["topic"])
            ok, why = q.add(target, f["query"], priority=it["priority"] - 0.5,
                            origin="relance_lacune", depth=it["depth"] + 1,
                            parent=it["key"], reason=f["reason"])
            if ok:
                follow.append({**f, "topic": target})
                summary["followups_added"] += 1
    result = {"returned": st.get("returned", 0), "fetched": st.get("fetched", 0), "created": st.get("created", 0),
              'fetch_attempts': st.get('fetch_attempts', st.get('fetched', 0)),
              'http_calls': q.daily()['http_calls'] - http_before,
              "rejected": st.get("rejected", 0), "duplicates": st.get("duplicates", 0), "updated": st.get("updated", 0),
              "notes": [n["id"] for n in notes], "followups": [f["query"] for f in follow], "errors": len(st.get("errors", [])),
              'stagnation': stagnation, 'knowledge_available': any(
                  n['evaluation']['diagnostics']['source_traceability'] and n['evaluation']['diagnostics']['actionable_steps']
                  and n.get('status') not in ('rejete', 'obsolete') for n in notes),
              'expansion_stop': 'stagnation' if stagnation >= cfg['queue']['stagnation_limit'] else
                                'max_depth' if it['depth'] >= cfg['queue']['max_depth'] else None}
    if st.get('stop_reason'):
        q.mark_failed(it, st['stop_reason'])
        return {**out, **result, 'status': 'interrompu', 'stop_reason': st['stop_reason'], 'notes': notes, 'followups': follow}
    if st.get('errors') and not st.get('fetched', 0) and not st.get('duplicates', 0):
        q.mark_failed(it, '; '.join(st['errors']))
        return {**out, **result, 'status': 'echec', 'notes': notes, 'followups': follow}
    q.mark_done(it, result)
    return {**out, **{k: result[k] for k in ("created", "rejected", "duplicates", "fetched")}, "notes": notes, "followups": follow}


def queue_status(root: Path = ROOT) -> dict:
    return ResearchQueue(Path(root), recover=False).summary()
