"""Méta-recherche mesurable : comparaison de stratégies de requête, mémoire, régressions, journal. Pas de LLM.

V5 : chaque essai enregistre des métriques SÉPARÉES (résultats, acceptés, nouveaux, hors sujet, doublons, erreurs,
passages techniques, durée). La « récompense » utilisée pour choisir une stratégie est calculée à partir de ces
métriques, mais toutes restent visibles dans le rapport : aucun score opaque unique.

Une stratégie ne change QUE la formulation des requêtes ; aucun code n'est modifié automatiquement.
Retour arrière : si une stratégie régresse nettement, l'agent revient à « terms » et le consigne dans le journal.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = ("terms", "synonyms", "facet")
LEGACY = ("baseline", "focused", "site_specific")


def save_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def reward_of(m: dict) -> float:
    """Récompense d'un essai, explicable : part de résultats utiles NOUVEAUX, modulée par le contenu technique,
    pénalisée par le hors-sujet et les erreurs. Bornée à [0, 1]."""
    returned = m.get("returned", 0)
    if m.get("error"):
        return 0.0
    if not returned:
        return 0.0
    useful = (m.get("new", 0) + 0.3 * m.get("updated", 0)) / returned
    tech = m.get("technical_mean") or 0.0
    off = m.get("offtopic", 0) / returned
    return round(max(0.0, min(1.0, 0.6 * useful + 0.4 * tech - 0.2 * off)), 4)


def _arm(state, provider, topic, strategy):
    return state.setdefault("arms", {}).setdefault(f"{provider}:{topic}", {}).setdefault(
        strategy, {"n": 0, "reward": 0.0, "returned": 0, "accepted": 0, "new": 0, "offtopic": 0, "duplicates": 0,
                   "errors": 0, "empty": 0, "recent": []})


def record_trial(state: dict, provider: str, topic: str, strategy: str, m: dict) -> float:
    r = reward_of(m)
    a = _arm(state, provider, topic, strategy)
    a["n"] += 1
    a["reward"] += r
    for k in ("returned", "accepted", "new", "offtopic", "duplicates"):
        a[k] = a.get(k, 0) + int(m.get(k, 0))
    a["errors"] = a.get("errors", 0) + (1 if m.get("error") else 0)
    a["empty"] = a.get("empty", 0) + (1 if not m.get("returned") else 0)
    a["recent"] = (a.get("recent", []) + [r])[-8:]
    a["best_mean"] = max(a.get("best_mean", 0.0), a["reward"] / a["n"])
    return r


def choose(state: dict, provider: str, topic: str, journal: list | None = None) -> str:
    """UCB1 déterministe : chaque stratégie est d'abord essayée une fois, puis exploitation/exploration.
    Une stratégie dont les 5 derniers essais tombent sous la moitié de sa meilleure moyenne (≥ 8 essais) est
    mise de côté au profit de « terms » (retour arrière consigné)."""
    arms = state.get("arms", {}).get(f"{provider}:{topic}", {})
    for name in STRATEGIES:
        if arms.get(name, {}).get("n", 0) == 0:
            return name
    usable = []
    for name in STRATEGIES:
        a = arms[name]
        recent = a.get("recent", [])
        if name != "terms" and a["n"] >= 8 and len(recent) >= 5 and a.get("best_mean", 0) > 0 and \
                sum(recent[-5:]) / 5 < 0.5 * a["best_mean"]:
            if journal is not None:
                journal.append({"event": "regression", "arm": f"{provider}:{topic}:{name}",
                                "recent_mean": round(sum(recent[-5:]) / 5, 4), "best_mean": round(a["best_mean"], 4),
                                "action": "retour à « terms »"})
            continue
        usable.append(name)
    total = sum(arms[x]["n"] for x in usable) or 1
    return max(usable, key=lambda x: (arms[x]["reward"] / arms[x]["n"] + 0.5 * math.sqrt(math.log(total + 1) / arms[x]["n"]),
                                      -STRATEGIES.index(x)))


def journal_append(root: Path, entries: list):
    if not entries:
        return
    p = Path(root) / "output" / "meta_journal.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    with p.open("a", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps({"utc": ts, **e}, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ compatibilité V4 (anciens tests et état)
def relevance(item, query, topic):
    from agent import relevance as rel
    return rel.assess(query, str(item.get("title", "")), str(item.get("excerpt", "")), provider="devforum")["topical"]


def record(state, provider, topic, strategy, rewards):
    key = f"{provider}:{topic}"
    arm = state.setdefault("arms", {}).setdefault(key, {}).setdefault(strategy, {"n": 0, "reward": 0.0})
    arm["n"] += 1
    arm["reward"] += sum(rewards) / max(1, len(rewards))
    arm["empty"] = arm.get("empty", 0) + (1 if not rewards else 0)
    arm["returned"] = arm.get("returned", 0) + len(rewards)


def queries(q, provider):
    """Compatibilité V4 : les trois anciennes formulations, désormais toutes courtes (plus de « language:Python »)."""
    from agent.planner import variants
    v = variants(q)
    return {**v, "baseline": v["terms"], "focused": v["facet"], "site_specific": v["synonyms"]}


def assess(items, query, topic, threshold=0.40):
    evaluated = [{"title": i.get("title", ""), "url": i.get("url", ""), "relevance": relevance(i, query, topic)} for i in items]
    return evaluated, [i for i, e in zip(items, evaluated) if e["relevance"] >= threshold]


def trial_metrics(evaluated, accepted, new_count=0, error=None):
    scores = [float(x.get("relevance", 0)) for x in evaluated]
    return {"returned": len(evaluated), "accepted": len(accepted), "rejected": len(evaluated) - len(accepted),
            "new": new_count, "avg_relevance": round(sum(scores) / len(scores), 4) if scores else None,
            "error": str(error)[:200] if error else None}


def report(root=ROOT):
    root = Path(root)
    p = root / "output" / "meta_state.json"
    state = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    lines = ["# VDN — Rapport méta-recherche (V5)", "",
             "Récompense = 0,6 × part de résultats nouveaux utiles + 0,4 × contenu technique − 0,2 × hors sujet (0 si erreur). "
             "Elle mesure l'UTILITÉ APPARENTE des requêtes, pas la véracité ni la validation dans Roblox.", "",
             "| Source:sujet | Stratégie | Essais | Retournés | Acceptés | Nouveaux | Hors sujet | Doublons | Erreurs | Vides | Récompense moy. |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for key, arms in sorted(state.get("arms", {}).items()):
        for name, v in sorted(arms.items()):
            if name in LEGACY:
                continue
            n = v.get("n", 0) or 1
            lines.append(f"| {key} | {name} | {v.get('n', 0)} | {v.get('returned', 0)} | {v.get('accepted', 0)} | {v.get('new', 0)} | "
                         f"{v.get('offtopic', 0)} | {v.get('duplicates', 0)} | {v.get('errors', 0)} | {v.get('empty', 0)} | {v.get('reward', 0) / n:.3f} |")
    legacy = [(k, n) for k, arms in state.get("arms", {}).items() for n in arms if n in LEGACY]
    if legacy:
        lines += ["", f"_{len(legacy)} anciennes stratégies V4 (baseline/focused/site_specific) conservées dans l'état, "
                      "non utilisées : elles étaient évaluées avec un calcul de pertinence défectueux (titre seul)._"]
    last = root / "output" / "last_run.json"
    if last.exists():
        try:
            run = json.loads(last.read_text(encoding="utf-8"))
            lines += ["", "## Dernière exécution", "",
                      f"- Requêtes logiques : {run.get('queries', '?')} (chacune envoyée à chaque fournisseur actif : "
                      f"{run.get('trials', '?')} essais au total)",
                      f"- Résultats renvoyés : {run.get('returned', '?')} · lus : {run.get('fetched', '?')} · acceptés : {run.get('accepted', '?')}",
                      f"- Fiches créées : {run.get('created', '?')} · mises à jour : {run.get('updated', '?')} · rejetées : {run.get('rejected', '?')}",
                      f"- Erreurs : {len(run.get('errors', []))}", ""]
            if run.get("rejection_reasons"):
                lines += ["### Raisons de rejet les plus fréquentes", ""]
                for reason, count in sorted(run["rejection_reasons"].items(), key=lambda x: -x[1])[:8]:
                    lines.append(f"- {count} × {reason}")
                lines.append("")
            if run.get("errors"):
                lines += ["### Erreurs", ""] + [f"- {e}" for e in run["errors"][:15]] + [""]
        except (ValueError, OSError):
            pass
    lines += ["## Sécurité et limites", "", "- Aucune modification automatique de code ; aucune exécution de code venant du web.",
              "- Le contenu des sources est une donnée, jamais une instruction.",
              "- Retour arrière : supprimer output/meta_state.json remet toutes les stratégies à zéro.", ""]
    (root / "output").mkdir(parents=True, exist_ok=True)
    (root / "output" / "meta_report.md").write_text("\n".join(lines), encoding="utf-8")
    return state


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    report()
