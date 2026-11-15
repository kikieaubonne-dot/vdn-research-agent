"""Benchmark annoté et détection de régressions. Ne prétend à aucune supériorité sans ces mesures.

Hors ligne (toujours, aussi dans GitHub Actions) :
  1. Filtre de pertinence : cas RÉELS étiquetés à la main (bench/relevance_cases.json) -> précision, rappel, F1.
  2. RAG : questions FR/EN avec fiche attendue (bench/rag_queries.json) -> réussite@1, réussite@3, MRR, tokens ;
     questions « négatives » : le bruit rejeté ne doit jamais sortir.
  3. Planificateur : toutes les requêtes doivent faire 2 à 4 termes (cause principale de l'échec V4.1).
En ligne (--online, sur le PC ou dans Actions) :
  4. Fournisseurs : pour des questions dont la page officielle attendue est connue, la page sort-elle dans les 5 premiers ?

Historique : output/benchmark_history.jsonl. Régression = baisse d'un indicateur au-delà de la tolérance par rapport
au meilleur passage précédent sur les MÊMES jeux de test (empreinte des fichiers de test).
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path

from agent import planner, rag, relevance
from agent.text import tokens

ROOT = Path(__file__).resolve().parents[1]
TOLERANCE = {"relevance_f1": 0.05, "relevance_precision": 0.05, "rag_hit_at_3": 0.05, "rag_mrr": 0.05, "negatives_clean": 0.0,
             "planner_ok": 0.0, "online_hit_at_5": 0.1}
ONLINE_CASES = [
    {"q": "SurfaceAppearance AlphaMode transparency", "provider": "roblox_docs", "expect": ["surface-appearance", "SurfaceAppearance"]},
    {"q": "atmosphere density haze", "provider": "roblox_docs", "expect": ["environment/atmosphere", "Atmosphere"]},
    {"q": "global wind", "provider": "roblox_docs", "expect": ["global-wind", "GlobalWind"]},
    {"q": "instance streaming", "provider": "roblox_docs", "expect": ["workspace/streaming"]},
    {"q": "terrain custom materials", "provider": "roblox_docs", "expect": ["custom-terrain-materials", "MaterialVariant"]},
    {"q": "texture specifications", "provider": "roblox_docs", "expect": ["texture-specifications"]},
]


def _fingerprint(*paths: Path) -> str:
    h = hashlib.sha256()
    for p in paths:
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:12]


def bench_relevance(root: Path) -> dict:
    data = json.loads((root / "bench" / "relevance_cases.json").read_text(encoding="utf-8"))["cases"]
    tp = fp = fn = tn = 0
    errors = []
    for c in data:
        a = relevance.assess(c["query"], c["title"], c["evidence"], provider=c.get("provider", ""))
        # « candidat à relire » (sujet OK, extrait trop court) compte comme accepté, comme dans la migration
        accepted = a["accepted"] or (a["topical"] >= relevance.ACCEPT["topical"] and a["roblox"] and not a["noise"])
        if accepted and c["label"]:
            tp += 1
        elif accepted and not c["label"]:
            fp += 1
            errors.append({"type": "faux positif", "title": c["title"], "note": c.get("note", "")})
        elif not accepted and c["label"]:
            fn += 1
            errors.append({"type": "faux négatif", "title": c["title"], "reasons": a["reasons"], "note": c.get("note", "")})
        else:
            tn += 1
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return {"cases": len(data), "tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": round(p, 3), "recall": round(r, 3),
            "f1": round(f1, 3), "errors": errors}


def bench_rag(root: Path) -> dict:
    rag.update_index(root)
    data = json.loads((root / "bench" / "rag_queries.json").read_text(encoding="utf-8"))
    hits1 = hits3 = 0
    rr, toks, misses = [], [], []
    for c in data["queries"]:
        res = rag.search_knowledge(c["q"], top_k=5, token_budget=1500, root=root)
        ids = list(dict.fromkeys(r["note_id"] for r in res["results"]))
        toks.append(res["tokens_estimated"])
        rank = next((i + 1 for i, x in enumerate(ids) if x in c["expected"]), None)
        hits1 += rank == 1
        hits3 += bool(rank and rank <= 3)
        rr.append(1 / rank if rank else 0.0)
        if not rank or rank > 3:
            misses.append({"q": c["q"], "rank": rank, "got": ids[:3]})
    neg_ok = 0
    for c in data.get("negatives", []):
        res = rag.search_knowledge(c["q"], top_k=5, token_budget=1500, root=root)
        ids = {r["note_id"] for r in res["results"]}
        neg_ok += not (ids & set(c["must_not_return"]))
    n = len(data["queries"]) or 1
    return {"queries": len(data["queries"]), "hit_at_1": round(hits1 / n, 3), "hit_at_3": round(hits3 / n, 3),
            "mrr": round(sum(rr) / n, 3), "avg_tokens": round(sum(toks) / n), "max_tokens": max(toks or [0]),
            "negatives_clean": round(neg_ok / max(1, len(data.get("negatives", []))), 3), "misses": misses}


def bench_planner(root: Path) -> dict:
    bad = []
    for t in planner.load_topics(root):
        for q in t.get("queries", []):
            for name, v in planner.variants(q).items():
                n = len(v.split())
                if not 2 <= n <= 4:
                    bad.append(f"{t['id']} / {name} : « {v} » ({n} mots)")
    return {"ok": not bad, "bad": bad}


def bench_online(root: Path) -> dict:
    from agent.run import active_providers
    provs = active_providers(root)
    hits, details = 0, []
    for c in ONLINE_CASES:
        try:
            res = provs[c["provider"]].search(c["q"], 5)
            ok = any(any(e.lower() in (r["url"] + r["title"]).lower() for e in c["expect"]) for r in res)
            details.append({"q": c["q"], "ok": ok, "top": [r["url"] for r in res[:3]]})
        except Exception as e:
            ok = False
            details.append({"q": c["q"], "ok": False, "error": f"{type(e).__name__}: {e}"})
        hits += ok
    return {"cases": len(ONLINE_CASES), "hit_at_5": round(hits / len(ONLINE_CASES), 3), "details": details}


def run(root: Path = ROOT, online: bool = False) -> dict:
    root = Path(root)
    out = {"utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "fingerprint": _fingerprint(root / "bench" / "relevance_cases.json", root / "bench" / "rag_queries.json", root / "config" / "topics.json"),
           "relevance": bench_relevance(root), "rag": bench_rag(root), "planner": bench_planner(root)}
    if online:
        out["online"] = bench_online(root)
    metrics = {"relevance_f1": out["relevance"]["f1"], "relevance_precision": out["relevance"]["precision"],
               "rag_hit_at_3": out["rag"]["hit_at_3"], "rag_mrr": out["rag"]["mrr"],
               "negatives_clean": out["rag"]["negatives_clean"], "planner_ok": 1.0 if out["planner"]["ok"] else 0.0}
    if online:
        metrics["online_hit_at_5"] = out["online"]["hit_at_5"]
    out["metrics"] = metrics
    hist_path = root / "output" / "benchmark_history.jsonl"
    history = []
    if hist_path.exists():
        history = [json.loads(l) for l in hist_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    same = [h for h in history if h.get("fingerprint") == out["fingerprint"]]
    regressions = []
    for k, v in metrics.items():
        best = max((h["metrics"].get(k) for h in same if h["metrics"].get(k) is not None), default=None)
        if best is not None and v < best - TOLERANCE.get(k, 0.05):
            regressions.append({"metric": k, "now": v, "best": best})
    out["regressions"] = regressions
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    with hist_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"utc": out["utc"], "fingerprint": out["fingerprint"], "metrics": metrics}) + "\n")
    lines = ["# Benchmark VDN", "", f"_{out['utc']} · jeux de test {out['fingerprint']}_", "",
             "| Indicateur | Valeur |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in metrics.items()]
    rel = out["relevance"]
    lines += ["", f"Filtre de pertinence sur {rel['cases']} cas réels étiquetés à la main : VP {rel['tp']}, FP {rel['fp']}, "
              f"FN {rel['fn']}, VN {rel['tn']}.", ""]
    lines += [f"- {e['type']} : {e['title']} {('(' + e['note'] + ')') if e.get('note') else ''}" for e in rel["errors"]]
    r = out["rag"]
    lines += ["", f"RAG : {r['queries']} questions (FR/EN), réussite@1 {r['hit_at_1']}, réussite@3 {r['hit_at_3']}, MRR {r['mrr']}, "
              f"tokens moyens {r['avg_tokens']} (max {r['max_tokens']}), questions négatives propres {r['negatives_clean']}.", ""]
    lines += [f"- manqué : « {m['q']} » (rang {m['rank']})" for m in r["misses"]]
    if regressions:
        lines += ["", "## ⚠ Régressions", ""] + [f"- {x['metric']} : {x['now']} (meilleur {x['best']})" for x in regressions]
    lines += ["", "Limites : étiquettes posées par une seule personne (Claude) ; petit échantillon ; mesure le tri et la "
              "récupération, PAS la justesse des techniques ni leur rendu dans Roblox.", ""]
    (root / "output" / "benchmark_report.md").write_text("\n".join(lines), encoding="utf-8")
    return out
