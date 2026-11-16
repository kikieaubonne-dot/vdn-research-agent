"""VDN Research Agent V5 — point d'entrée unique.

    python -m agent.run research [--max-queries 8] [--per-source 4] [--max-fetch 30]   recherche (GitHub Actions ou PC)
    python -m agent.run refresh  [--devforum-pages 3]     index officiel Roblox + sitemap DevForum (hebdomadaire)
    python -m agent.run migrate                           reclasse les fiches V1–V4 (aucune suppression)
    python -m agent.run index                             index Obsidian + base de recherche (RAG)
    python -m agent.run enrich   [--max-notes 5]          analyse IA locale (Ollama), seulement si disponible
    python -m agent.run bench    [--online]               benchmark annoté + détection de régressions
    python -m agent.run ask "question"                    tester la recherche dans la bibliothèque (comme Claude)

Compteurs (sens précis, pour éviter l'ambiguïté V4.1) :
  queries  = requêtes logiques planifiées ; trials = requêtes × fournisseurs actifs ;
  returned = résultats renvoyés par les moteurs ; fetched = sources réellement lues ; accepted = sources retenues ;
  created / updated / duplicates / rejected = effet sur la bibliothèque.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

from agent import knowledge, meta, planner, providers, rag, relevance
from agent import budget
from agent.text import tokens, concepts

ROOT = Path(__file__).resolve().parents[1]


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
    except ValueError:
        return default


def active_providers(root: Path, getter=None) -> dict:
    g = getter or providers.http_get
    out = {"roblox_docs": providers.RobloxDocs(root, g), "devforum": providers.DevForum(root, g), "github": providers.GitHub(root, g)}
    sx = providers.SearXNG(getter=g)
    if sx.available():
        out["searxng"] = sx
    return out


def research(root: Path = ROOT, max_queries: int = 8, per_source: int = 4, max_fetch: int = 30, pause: float = 1.0, provs=None,
             planned=None, finalize: bool = True, touch_existing: bool = True) -> dict:
    """Un cycle de recherche. ``planned`` = [(topic, requete, origine)] impose le plan (file autonome V5.5) ;
    ``finalize=False`` saute la reconstruction des index (faite une seule fois en fin de cycle autonome) ;
    ``touch_existing=False`` ne modifie jamais une fiche deja creee (une source connue compte comme doublon)."""
    root = Path(root)
    state_path, meta_path = root / "output/state.json", root / "output/meta_state.json"
    state = load_json(state_path, {"seen": {}, "query_runs": {}, "runs": 0, "errors": []})
    mstate = load_json(meta_path, {})
    followups = [f for f in load_json(root / "output/followups.json", {"items": []})["items"] if f.get("status") == "open"]
    setup_errors = []
    setup_stop = None
    setup_stop_details = None
    if provs is None:
        provs = active_providers(root)
        # premier lancement : sans index local, la doc officielle et le DevForum ne peuvent rien trouver
        if not provs["roblox_docs"].path.exists():
            try:
                provs["roblox_docs"].refresh()
            except budget.BudgetExhausted as e:
                setup_stop = str(e)
                setup_stop_details = e.details()
            except Exception as e:
                setup_errors.append(f"index officiel indisponible (la doc Roblox ne sera pas interrogée) : {e}")
        if setup_stop is None and not provs["devforum"].index_path.exists():
            try:
                provs["devforum"].refresh(2)
            except budget.BudgetExhausted as e:
                setup_stop = str(e)
                setup_stop_details = e.details()
            except Exception as e:
                setup_errors.append(f"sitemap DevForum indisponible (le DevForum ne sera pas interrogé) : {e}")
    reg = knowledge.Registry(root)
    journal, rejected_log = [], []
    st = {"started_utc": utcnow(), "version": "5.0", "queries": 0, "trials": 0, "returned": 0, "fetched": 0, "accepted": 0,
          "created": 0, "updated": 0, "duplicates": 0, "rejected": 0, "errors": list(setup_errors), "rejection_reasons": {}, "trials_detail": [], "created_notes": [], "rejected_candidates": [],
          "providers": list(provs), "fetch_attempts": 0, "stop_reason": setup_stop, 'stop_details':setup_stop_details, 'known_notes': []}

    def stop_for(exc):
        st['stop_reason']=str(exc);st['stop_details']=exc.details()

    def stopped():
        if st['stop_reason']:
            return True
        try:
            budget.check()
        except budget.BudgetExhausted as e:
            stop_for(e)
            return True
        return False

    fetched_total = 0
    plan_items = planned if planned is not None else planner.plan(state, root, max_queries, followups)
    if planned is not None:
        followups = []  # la file autonome gere elle-meme ses relances
    for topic, query, origin in plan_items:
        if stopped() or st['queries'] >= max_queries:
            break
        st["queries"] += 1
        state["query_runs"][query] = state["query_runs"].get(query, 0) + 1
        topic_concepts = concepts(tokens(" ".join([topic.get("title", "")] + topic.get("subtopics", []))))
        for pname, prov in provs.items():
            if stopped():
                break
            strategy = meta.choose(mstate, pname, topic["id"], journal)
            q = planner.variants(query)[strategy]
            m = {"returned": 0, "accepted": 0, "new": 0, "updated": 0, "offtopic": 0, "duplicates": 0, "error": None, "technical": []}
            t0 = time.time()
            st["trials"] += 1
            try:
                results = prov.search(q, per_source)
            except budget.BudgetExhausted as e:
                stop_for(e)
                break
            except Exception as e:
                m["error"] = f"{type(e).__name__}: {str(e)[:150]}"
                st["errors"].append(f"{pname} / {q} : {m['error']}")
                results = []
            m["returned"] = len(results)
            st["returned"] += len(results)
            for item in results:
                if stopped():
                    break
                url = item.get("url", "")
                existing = reg.find(url)
                if existing:
                    if touch_existing:
                        res = knowledge.write_note(root, reg, topic, query, item, {}, {"accepted": True})
                    else:
                        res = {"action": "duplicate"}
                    key = "updated" if res["action"] == "updated" else "duplicates"
                    m[key] += 1
                    st[key] += 1
                    path = root / existing['path']
                    if path.exists() and existing['id'] not in {n['id'] for n in st['known_notes']}:
                        existing_meta, _ = knowledge.parse_note(path.read_text(encoding='utf-8'))
                        st['known_notes'].append({**existing, 'status': existing_meta.get('status')})
                    continue
                if fetched_total >= max_fetch:
                    break
                reader = providers.provider_for(url, provs) or prov
                try:
                    budget.fetch_attempt()
                    fetched_total += 1
                    st['fetch_attempts'] += 1
                    doc = reader.fetch(url)
                except budget.BudgetExhausted as e:
                    stop_for(e)
                    break
                except Exception as e:
                    st["errors"].append(f"lecture {url} : {type(e).__name__}: {str(e)[:120]}")
                    continue
                st["fetched"] += 1
                src = {**item, "provider": reader.name, "tier": 1 if doc.get("official") and reader.name == "devforum" else reader.tier}
                a = relevance.assess(query, doc.get("title") or item.get("title", ""), doc.get("text", ""), reader.name, topic_concepts)
                m["technical"].append(a["technical"])
                res = knowledge.write_note(root, reg, topic, query, src, doc, a)
                if res["action"] == "created":
                    m["new"] += 1
                    m["accepted"] += 1
                    st["accepted"] += 1
                    st["created"] += 1
                    st["created_notes"].append({"id": res["id"], "path": res["path"], "status": res["status"],
                                                "topic": topic["id"], "query": query, "url": providers.canonical_url(url)})
                else:
                    m["offtopic"] += 1
                    st["rejected"] += 1
                    for r in a.get("reasons", []) or ["doublon de contenu"]:
                        k = r.split("(")[0].strip()
                        st["rejection_reasons"][k] = st["rejection_reasons"].get(k, 0) + 1
                    st["rejected_candidates"].append({"topical": a["topical"], "technical": a["technical"],
                                                       "roblox": a["roblox"], "noise": a["noise"],
                                                       "reasons": a.get("reasons", [])})
                    rejected_log.append({"utc": st["started_utc"], "url": providers.canonical_url(url), "query": query,
                                         "provider": reader.name, "reasons": a.get("reasons"), "topical": a["topical"],
                                         "technical": a["technical"]})
                if pause:
                    try:
                        budget.pause(pause)
                    except budget.BudgetExhausted as e:
                        stop_for(e)
                        break
            m["technical_mean"] = round(sum(m["technical"]) / len(m["technical"]), 3) if m["technical"] else 0.0
            m["duration_s"] = round(time.time() - t0, 2)
            reward = meta.record_trial(mstate, pname, topic["id"], strategy, m)
            st["trials_detail"].append({"provider": pname, "topic": topic["id"], "origin": origin, "strategy": strategy, "query": q,
                                        **{k: m[k] for k in ("returned", "accepted", "new", "updated", "duplicates", "offtopic", "error",
                                                             "technical_mean", "duration_s")}, "reward": reward})
    for f in followups[: max(0, max_queries // 4)]:
        f["status"] = "done"
    fu = load_json(root / "output/followups.json", {"items": []})
    done = {f["query"] for f in followups[: max(0, max_queries // 4)]}
    for f in fu["items"]:
        if f["query"] in done:
            f["status"] = "done"
    (root / "output").mkdir(exist_ok=True)
    meta.save_json(root / "output/followups.json", fu)
    state["runs"] = int(state.get("runs", 0)) + 1
    state["errors"] = st["errors"][-20:]
    meta.save_json(state_path, state)
    meta.save_json(meta_path, mstate)
    reg.save()
    meta.journal_append(root, journal)
    if rejected_log:
        with (root / "output/rejected.jsonl").open("a", encoding="utf-8") as f:
            for r in rejected_log:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    st["finished_utc"] = utcnow()
    meta.save_json(root / "output/last_run.json", st)
    if not finalize:
        return st
    meta.report(root)
    knowledge.build_indexes(root)
    rag.update_index(root)
    (root / "output/README.md").write_text(
        f"# Rapport VDN V5 — {st['started_utc']}\n\nRequêtes : {st['queries']} · essais : {st['trials']} · renvoyés : {st['returned']} · "
        f"lus : {st['fetched']} · acceptés : {st['accepted']}\n\nFiches créées : {st['created']} · mises à jour : {st['updated']} · "
        f"rejetées : {st['rejected']} · erreurs : {len(st['errors'])}\n\nDétails : `meta_report.md`. Les fiches sont des pistes "
        "**non testées dans Roblox Studio**.\n", encoding="utf-8")
    return st


def refresh(root: Path = ROOT, devforum_pages: int = 3) -> dict:
    from agent.autonomy import Lock
    from agent.research_queue import ResearchQueue, load_config
    root = Path(root)
    cfg = load_config(root)
    out = {}
    with Lock(root, cfg['lock']['stale_after_s']):
        q = ResearchQueue(root, cfg)
        daily = q.daily()
        def checkpoint(resource):
            if daily['http_calls'] >= cfg['daily']['max_http_calls']:
                raise budget.BudgetExhausted('quota quotidien HTTP atteint')
            daily['http_calls'] += 1
            q.save()
        guard = budget.Budget(cfg['cycle']['time_budget_s'], min(cfg['cycle']['max_http_calls'],
                              max(0, cfg['daily']['max_http_calls'] - daily['http_calls'])), checkpoint)
        with budget.using(guard):
            p = active_providers(root)
            for name, fn in (("roblox_docs", lambda: p["roblox_docs"].refresh()), ("devforum", lambda: p["devforum"].refresh(devforum_pages))):
                try:
                    out[name] = fn()
                except budget.BudgetExhausted as e:
                    out['stop_reason'] = str(e)
                    break
                except Exception as e:
                    out[name] = f"erreur : {type(e).__name__}: {str(e)[:150]} (cache précédent conservé)"
        out['http_calls'] = guard.http_calls
        meta.save_json(root / "output/last_refresh.json", {"utc": utcnow(), **out})
    return out


def enrich(root: Path = ROOT, max_notes: int = 5) -> dict:
    from agent import llm
    if not llm.available():
        return {"status": "Ollama indisponible : aucune analyse IA effectuée (rien n'est simulé).", "model": llm.MODEL}
    done, fu = [], load_json(Path(root) / "output/followups.json", {"items": []})
    notes = [n for n in knowledge.load_notes(root) if n.get("status") in ("documente", "candidat") and "## Analyse IA" not in n["_body"]]
    notes.sort(key=lambda n: (knowledge.STATUS_RANK.get(n.get("status"), 9), int(n.get("source_tier", 9) or 9)))
    for n in notes[:max_notes]:
        r = llm.enrich_note(Path(root) / n["_path"])
        done.append({"id": n["id"], **{k: v for k, v in r.items() if k != "questions"}})
        for q in r.get("questions", []) if isinstance(r, dict) else []:
            if q not in {x["query"] for x in fu["items"]}:
                fu["items"].append({"query": q, "topic": n.get("subdomain"), "from": n["id"], "status": "open"})
    meta.save_json(Path(root) / "output/followups.json", fu)
    knowledge.build_indexes(root)
    rag.update_index(root)
    return {"status": "ok", "model": llm.MODEL, "notes": done}


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="python -m agent.run", description="VDN Research Agent V5")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("research")
    r.add_argument("--max-queries", type=int, default=8)
    r.add_argument("--per-source", type=int, default=4)
    r.add_argument("--max-fetch", type=int, default=30)
    r.add_argument("--pause", type=float, default=1.0)
    f = sub.add_parser("refresh")
    f.add_argument("--devforum-pages", type=int, default=3)
    sub.add_parser("migrate")
    sub.add_parser("index")
    e = sub.add_parser("enrich")
    e.add_argument("--max-notes", type=int, default=5)
    b = sub.add_parser("bench")
    b.add_argument("--online", action="store_true")
    b.add_argument("--no-fail", action="store_true", help="ne pas renvoyer d'erreur en cas de régression")
    c = sub.add_parser("cycle", help="un cycle autonome borne (V5.5)")
    c.add_argument("--max-items", type=int, default=None)
    c.add_argument("--time-budget", type=float, default=None)
    sub.add_parser("queue", help="etat de la file autonome")
    p = sub.add_parser('plan', help='decomposer une question en recherches avec prerequis, sans reseau')
    p.add_argument('question')
    p.add_argument('--topic', required=True)
    sub.add_parser('evaluate', help='diagnostic des fiches, sans modifier leurs statuts')
    k = sub.add_parser("ask")
    k.add_argument("query")
    k.add_argument("--top-k", type=int, default=5)
    k.add_argument("--budget", type=int, default=1500)
    a = ap.parse_args(argv)
    if a.cmd == "research":
        if not (1 <= a.max_queries <= 30 and 1 <= a.per_source <= 10 and 1 <= a.max_fetch <= 100 and a.pause >= 0):
            ap.error("limites : max-queries 1..30, per-source 1..10, max-fetch 1..100, pause ≥ 0")
        out = research(ROOT, a.max_queries, a.per_source, a.max_fetch, a.pause)
        out = {k: v for k, v in out.items() if k != "trials_detail"}
    elif a.cmd == "refresh":
        out = refresh(ROOT, a.devforum_pages)
    elif a.cmd == "migrate":
        out = knowledge.migrate_legacy(ROOT)
        out["index"] = knowledge.build_indexes(ROOT)
        out["rag"] = rag.update_index(ROOT)
    elif a.cmd == "index":
        out = {"domains": knowledge.build_indexes(ROOT), "rag": rag.update_index(ROOT)}
    elif a.cmd == "enrich":
        out = enrich(ROOT, a.max_notes)
    elif a.cmd == "cycle":
        from agent import autonomy
        if a.max_items is not None and not 1 <= a.max_items <= 20:
            ap.error("limite : max-items 1..20")
        out = autonomy.cycle(ROOT, max_items=a.max_items, time_budget_s=a.time_budget)
    elif a.cmd == "queue":
        from agent import autonomy
        out = autonomy.queue_status(ROOT)
    elif a.cmd == 'plan':
        from agent.autonomy import Lock
        from agent.research_queue import load_config
        from agent.decomposition import plan
        with Lock(ROOT, load_config(ROOT)['lock']['stale_after_s']):
            out = plan(ROOT, a.question, a.topic)
    elif a.cmd == 'evaluate':
        from agent.evaluation import evaluate_library
        out = evaluate_library(ROOT)
        meta.save_json(ROOT / 'output' / 'knowledge_evaluation.json', out)
    elif a.cmd == "bench":
        from agent import benchmark
        out = benchmark.run(ROOT, online=a.online)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 1 if out.get("regressions") and not a.no_fail else 0
    else:
        rag.update_index(ROOT)
        out = rag.search_knowledge(a.query, a.top_k, a.budget, root=ROOT)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
