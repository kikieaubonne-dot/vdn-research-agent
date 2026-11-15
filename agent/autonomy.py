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
from pathlib import Path

from agent import knowledge, meta, rag
from agent.followup_rules import followups_for_note, missing_info
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

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    json.dump({"pid": os.getpid(), "started": iso(), "ts": now_ts()}, f)
                return self
            except FileExistsError:
                try:
                    info = json.loads(self.path.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    info = {"ts": 0}
                if now_ts() - float(info.get("ts", 0)) <= self.stale:
                    raise Busy(f"un cycle est deja en cours (depuis {info.get('started', '?')})")
                self.path.unlink(missing_ok=True)
                self.took_over = True
        raise Busy("verrou impossible a obtenir")

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)
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


# ---------------------------------------------------------------------------- cycle
def cycle(root: Path = ROOT, provs=None, max_items: int | None = None, time_budget_s: float | None = None,
          research_fn=None) -> dict:
    """Un cycle autonome complet. ``provs`` et ``research_fn`` permettent les tests hors ligne."""
    root = Path(root)
    cfg = load_config(root)
    if research_fn is None:
        from agent.run import research as research_fn
    c = cfg["cycle"]
    max_items = int(max_items if max_items is not None else c["max_items"])
    budget = float(time_budget_s if time_budget_s is not None else c["time_budget_s"])
    t0 = now_ts()
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
            daily = q.daily()
            room = min(max_items, max(0, cfg["daily"]["max_items"] - daily["items"]))
            batch = q.next_batch(room)
            if not batch:
                summary["stop_reason"] = "quota quotidien atteint" if room == 0 else "file vide"
            for it in batch:
                if now_ts() - t0 > budget:
                    summary["stop_reason"] = "budget de temps atteint"
                    break
                if daily["fetch"] >= cfg["daily"]["max_fetch"]:
                    summary["stop_reason"] = "quota de lectures atteint"
                    break
                summary["items"].append(_run_item(root, q, it, cfg, provs, research_fn, summary))
                daily["items"] += 1
                q.save()
            summary["stop_reason"] = summary["stop_reason"] or "cycle termine"
            try:
                (root / "knowledge").mkdir(parents=True, exist_ok=True)
                knowledge.build_indexes(root)
                rag.update_index(root)
            except Exception as e:  # l'index se reconstruira au cycle suivant
                log_error(root, "index", e)
                summary["errors"].append(f"index : {type(e).__name__}: {e}")
            summary["queue"] = q.summary()
    except Busy as e:
        summary["stop_reason"] = str(e)
        summary["queue"] = ResearchQueue(root, cfg).summary() if (root / "output" / "queue.json").exists() else \
            {"counts": {"pending": 0, "done": 0}, "daily": {"items": 0}, "next": []}
        summary["finished"] = iso()
        return summary
    summary["finished"] = iso()
    meta.save_json(root / "output" / "last_cycle.json", summary)
    summary["report"] = str(write_daily_report(root, summary).relative_to(root)).replace("\\", "/")
    return summary


def _run_item(root: Path, q: ResearchQueue, it: dict, cfg: dict, provs, research_fn, summary: dict) -> dict:
    topic = q.topics[it["topic"]]
    c = cfg["cycle"]
    out = {"query": it["query"], "topic": it["topic"], "depth": it["depth"], "origin": it["origin"], "status": "done"}
    q.mark_running(it)
    try:
        st = research_fn(root, max_queries=1, per_source=c["per_source"], max_fetch=c["max_fetch_per_item"],
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
    q.daily()["fetch"] += st.get("fetched", 0)
    summary["fetched"] += st.get("fetched", 0)
    summary["created"] += st.get("created", 0)
    summary["rejected"] += st.get("rejected", 0)
    notes, follow = [], []
    for n in st.get("created_notes", []):
        path = root / n["path"]
        body = path.read_text(encoding="utf-8") if path.exists() else ""
        notes.append({**n, "missing": missing_info(body)})
        if not path.exists() or it["depth"] >= cfg["queue"]["max_depth"]:
            continue
        for f in followups_for_note(path, it["query"], cfg["queue"]["max_children_per_note"]):
            target = q.best_topic(f["query"], it["topic"])
            ok, why = q.add(target, f["query"], priority=it["priority"] - 0.5, origin="relance",
                            depth=it["depth"] + 1, parent=it["key"], reason=f["reason"])
            if ok:
                follow.append({**f, "topic": target})
                summary["followups_added"] += 1
    result = {"returned": st.get("returned", 0), "fetched": st.get("fetched", 0), "created": st.get("created", 0),
              "rejected": st.get("rejected", 0), "duplicates": st.get("duplicates", 0), "updated": st.get("updated", 0),
              "notes": [n["id"] for n in notes], "followups": [f["query"] for f in follow], "errors": len(st.get("errors", []))}
    q.mark_done(it, result)
    return {**out, **{k: result[k] for k in ("created", "rejected", "duplicates", "fetched")}, "notes": notes, "followups": follow}


def queue_status(root: Path = ROOT) -> dict:
    return ResearchQueue(Path(root)).summary()
