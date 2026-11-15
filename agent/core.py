"""Free, bounded research collector. Standard library only; no LLM or paid API.

Data from third-party sites is treated as untrusted evidence, not instructions.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "VDNResearchAgent/1.0 (educational research; contact via repository issues)"
MAX_BYTES = 1_000_000


def utcnow():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urlopen(req, timeout=16) as response:
        if int(response.headers.get("Content-Length", "0")) > MAX_BYTES:
            raise ValueError("Response too large")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise ValueError("Response too large")
        return json.loads(data)


def clean(value, limit=400):
    text = html.unescape(re.sub(r"<[^>]*>", " ", str(value or "")))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def safe_filename(value):
    slug = re.sub(r"[^a-z0-9-]", "-", value.lower())
    return re.sub(r"-+", "-", slug).strip("-")[:70] or "topic"


def valid_url(value):
    try:
        p = urlparse(value)
        return p.scheme == "https" and bool(p.netloc) and not p.username and not p.password
    except ValueError:
        return False


def search_devforum(query, limit):
    # Discourse public search endpoint; may rate-limit or reject automated requests.
    data = fetch_json("https://devforum.roblox.com/search.json?q=" + quote(query))
    topics = {t.get("id"): t for t in data.get("topics", [])}
    out = []
    for post in data.get("posts", [])[:limit]:
        t = topics.get(post.get("topic_id"), {})
        slug = t.get("slug") or post.get("topic_slug") or "topic"
        tid = post.get("topic_id")
        if not tid:
            continue
        out.append({"title": clean(t.get("title") or post.get("blurb") or query, 160),
                    "url": f"https://devforum.roblox.com/t/{slug}/{tid}",
                    "excerpt": clean(post.get("blurb"), 350), "source": "Roblox DevForum"})
    return out


def search_github(query, limit):
    # GitHub public repository search; unauthenticated rate limits apply.
    data = fetch_json("https://api.github.com/search/repositories?q=" + quote(query + " in:name,description,readme") + "&per_page=" + str(limit))
    return [{"title": clean(x.get("full_name"), 160), "url": x.get("html_url", ""),
             "excerpt": clean(x.get("description"), 350), "source": "GitHub repositories"}
            for x in data.get("items", [])[:limit]]


def score(item, query, topic):
    haystack = (item["title"] + " " + item["excerpt"]).lower()
    words = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 3]
    overlap = sum(w in haystack for w in set(words))
    # Relevance heuristic, NOT proof of technical correctness or compatibility.
    return min(100, 15 + overlap * 10 + int(topic.get("priority", 5)) * 2)


def load_state(path):
    if path.exists():
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(state, dict) and isinstance(state.get("seen", {}), dict):
                return state
        except (OSError, ValueError):
            pass
    return {"seen": {}, "query_runs": {}, "runs": 0, "errors": []}


def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def markdown_escape(s):
    return clean(s, 600).replace("[", "\\[").replace("]", "\\]")


def note(item, topic, query, timestamp):
    # Deliberately label all discoveries as unverified; no invented implementation details.
    title = markdown_escape(item["title"])
    excerpt = markdown_escape(item["excerpt"] or "Aucun extrait disponible.")
    url = item["url"]
    return (f"---\nstatus: a_verifier\nsource_type: {json.dumps(item['source'], ensure_ascii=False)}\n"
            f"topic: {json.dumps(topic['id'])}\nscore_heuristique: {item['score']}\n"
            f"collected_utc: {json.dumps(timestamp)}\n---\n\n"
            f"# {title}\n\n**Sujet :** {markdown_escape(topic['title'])}\n\n"
            f"**Source :** [{markdown_escape(item['source'])}]({url})\n\n"
            f"**Question de recherche :** {markdown_escape(query)}\n\n"
            f"## Extrait de découverte (non vérifié)\n\n{excerpt}\n\n"
            "## Vérification Roblox / Blender\n\n"
            "- [ ] Ouvrir et lire la source complète\n"
            "- [ ] Vérifier la version du moteur et les limites techniques\n"
            "- [ ] Extraire une procédure précise, des paramètres et les prérequis\n"
            "- [ ] Tester dans Blender puis Roblox Studio\n"
            "- [ ] Mesurer visuel, performances et reproductibilité\n\n"
            "## Résultat du test\n\nÀ compléter après expérimentation.\n")


def run(root=ROOT, max_queries=8, per_source=3, pause=2.0):
    root = Path(root)
    cfg = json.loads((root / "config/topics.json").read_text(encoding="utf-8"))
    state_path = root / "output/state.json"
    state = load_state(state_path)
    now = utcnow()
    candidates = []
    for topic in cfg["topics"]:
        for query in topic["queries"]:
            candidates.append((int(state["query_runs"].get(query, 0)), -int(topic["priority"]), topic, query))
    candidates.sort(key=lambda x: (x[0], x[1], x[3]))
    picked = candidates[:max_queries]
    stats = {"started_utc": now, "queries": 0, "discovered": 0, "errors": [], "sources": {}}
    for _, _, topic, query in picked:
        stats["queries"] += 1
        state["query_runs"][query] = int(state["query_runs"].get(query, 0)) + 1
        for name, search in (("devforum", search_devforum), ("github", search_github)):
            try:
                items = search(query, per_source)
                stats["sources"][name] = stats["sources"].get(name, 0) + len(items)
                for item in items:
                    url = item.get("url", "")
                    if not valid_url(url):
                        continue
                    key = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
                    if key in state["seen"]:
                        continue
                    item["score"] = score(item, query, topic)
                    folder = root / "knowledge" / safe_filename(topic["id"])
                    folder.mkdir(parents=True, exist_ok=True)
                    filename = f"{key}-{safe_filename(item['title'])[:45]}.md"
                    (folder / filename).write_text(note(item, topic, query, now), encoding="utf-8")
                    state["seen"][key] = {"url": url, "topic": topic["id"], "date": now}
                    stats["discovered"] += 1
            except Exception as exc:
                stats["errors"].append(f"{name} / {query}: {type(exc).__name__}: {str(exc)[:150]}")
            if pause:
                time.sleep(pause)
    state["runs"] = int(state.get("runs", 0)) + 1
    state["errors"] = stats["errors"][-20:]
    save_json(state_path, state)
    save_json(root / "output/last_run.json", stats)
    report = (f"# Rapport VDN — {now}\n\nRecherches : {stats['queries']}  \n"
              f"Nouvelles fiches : {stats['discovered']}  \n"
              f"Erreurs : {len(stats['errors'])}\n\n"
              "Les fiches sont des pistes à vérifier, **pas** des techniques validées.\n")
    (root / "output/README.md").write_text(report, encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return stats


def main():
    p = argparse.ArgumentParser(description="VDN Research Agent")
    p.add_argument("--max-queries", type=int, default=int(os.getenv("VDN_MAX_QUERIES", "8")))
    p.add_argument("--per-source", type=int, default=int(os.getenv("VDN_PER_SOURCE", "3")))
    p.add_argument("--pause", type=float, default=2.0)
    args = p.parse_args()
    if not (1 <= args.max_queries <= 30 and 1 <= args.per_source <= 10 and args.pause >= 0):
        p.error("Use max-queries 1..30, per-source 1..10, pause >= 0")
    run(max_queries=args.max_queries, per_source=args.per_source, pause=args.pause)


if __name__ == "__main__":
    main()
