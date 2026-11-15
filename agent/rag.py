"""Index de recherche local pour Claude : SQLite FTS5 (BM25), mise à jour incrémentale, budget de tokens.

API (lecture seule) :
    search_knowledge(query, top_k=5, token_budget=1500)  -> passages courts classés
    read_knowledge(note_id, token_budget=3000)           -> une fiche (tronquée au budget)
    get_topic_index(topic)                               -> l'index Obsidian d'un domaine

Classement final = BM25 (titres pondérés) × poids du statut × poids de la confiance × poids du niveau de source
× fraîcheur. Les fiches « rejetées » sont exclues par défaut. Recherche progressive : tous les termes (ET),
puis n'importe lequel (OU), puis préfixes.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import re
import sqlite3
from pathlib import Path

from agent.knowledge import load_notes, sections, parse_note
from agent.text import tokens, approx_tokens, fold, expand

ROOT = Path(__file__).resolve().parents[1]
STATUS_W = {"valide": 1.6, "reproduit": 1.4, "documente": 1.15, "candidat": 0.8, "obsolete": 0.3, "rejete": 0.0}
CONF_W = {"haute": 1.3, "moyenne": 1.1, "faible": 0.9}
TIER_W = {1: 1.25, 2: 1.1, 3: 0.95, 4: 0.85}
SKIP_SECTIONS = {"Scores (diagnostic, pas une preuve)", "Tests dans Roblox Studio"}


def db_path(root: Path = ROOT) -> Path:
    p = Path(root) / "output" / "knowledge.db"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def connect(root: Path = ROOT) -> sqlite3.Connection:
    con = sqlite3.connect(db_path(root))
    con.execute("""CREATE TABLE IF NOT EXISTS notes(id TEXT PRIMARY KEY, path TEXT, title TEXT, domain TEXT, status TEXT,
                   confidence TEXT, tier INTEGER, updated TEXT, hash TEXT)""")
    try:
        con.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS passages USING fts5(note_id UNINDEXED, title, heading, body,
                       tokenize='unicode61 remove_diacritics 2')""")
        con.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")
        con.execute("INSERT OR REPLACE INTO meta VALUES('fts','5')")
    except sqlite3.OperationalError:
        # SQLite sans FTS5 (rare) : table simple, recherche par LIKE (plus lente mais fonctionnelle)
        con.execute("CREATE TABLE IF NOT EXISTS passages(note_id TEXT, title TEXT, heading TEXT, body TEXT)")
        con.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")
        con.execute("INSERT OR REPLACE INTO meta VALUES('fts','0')")
    return con


def has_fts(con) -> bool:
    row = con.execute("SELECT v FROM meta WHERE k='fts'").fetchone()
    return bool(row and row[0] == "5")


def _chunks(body: str, max_chars: int = 900) -> list[tuple[str, str]]:
    """Découpe une fiche en passages (section -> morceaux de ≤ max_chars, coupés sur les lignes)."""
    out = []
    for heading, text in sections(body).items():
        if heading in SKIP_SECTIONS or not text.strip():
            continue
        buf = ""
        for line in text.splitlines():
            if len(buf) + len(line) > max_chars and buf:
                out.append((heading, buf.strip()))
                buf = ""
            buf += line + "\n"
        if buf.strip():
            out.append((heading, buf.strip()))
    return out


def update_index(root: Path = ROOT) -> dict:
    """Mise à jour incrémentale : seules les fiches modifiées (empreinte du contenu) sont réindexées."""
    con = connect(root)
    known = {r[0]: r[1] for r in con.execute("SELECT id, hash FROM notes")}
    seen, added, changed = set(), 0, 0
    for n in load_notes(root):
        nid = str(n["id"])
        seen.add(nid)
        h = hashlib.sha256((json.dumps({k: v for k, v in n.items() if k != "_body"}, sort_keys=True, default=str) + n["_body"]).encode()).hexdigest()
        if known.get(nid) == h:
            continue
        con.execute("DELETE FROM passages WHERE note_id=?", (nid,))
        con.execute("INSERT OR REPLACE INTO notes VALUES(?,?,?,?,?,?,?,?,?)",
                    (nid, n["_path"], str(n.get("title", "")), str(n.get("domain", "")), str(n.get("status", "")),
                     str(n.get("confidence", "")), int(n.get("source_tier", 4) or 4), str(n.get("updated", "")), h))
        for heading, text in _chunks(n["_body"]):
            con.execute("INSERT INTO passages(note_id, title, heading, body) VALUES(?,?,?,?)", (nid, str(n.get("title", "")), heading, text))
        if nid in known:
            changed += 1
        else:
            added += 1
    removed = [x for x in known if x not in seen]
    for nid in removed:
        con.execute("DELETE FROM passages WHERE note_id=?", (nid,))
        con.execute("DELETE FROM notes WHERE id=?", (nid,))
    con.commit()
    total = con.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    con.close()
    return {"added": added, "changed": changed, "removed": len(removed), "notes": total}


def _fts_query(words: list[str], mode: str) -> str:
    safe = [re.sub(r"[^a-z0-9_]", "", w) for w in words]
    safe = [w for w in safe if w]
    if not safe:
        return ""
    if mode == "and":
        return " AND ".join(f'"{w}"' for w in safe)
    if mode == "or":
        return " OR ".join(f'"{w}"' for w in safe)
    return " OR ".join(f"{w}*" for w in safe if len(w) >= 3)


def _freshness(updated: str) -> float:
    try:
        days = (dt.date.today() - dt.date.fromisoformat(str(updated)[:10])).days
    except ValueError:
        return 0.9
    return 1.0 if days < 365 else 0.85 if days < 730 else 0.7


def search_knowledge(query: str, top_k: int = 5, token_budget: int = 1500, root: Path = ROOT,
                     include_rejected: bool = False, domain: str | None = None) -> dict:
    con = connect(root)
    raw = [fold(w) for w in re.findall(r"[\wÀ-ÿ]+", query) if len(w) > 1]
    words = [w for w in dict.fromkeys(tokens(query))]
    expanded = list(dict.fromkeys(words + [fold(s) for w in words for s in expand(w)][:12]))
    rows, mode_used, best_rows, best_mode = [], None, [], None
    for mode, terms in (("and", words), ("or", expanded), ("prefix", raw)):
        q = _fts_query(terms, mode)
        if not q:
            continue
        if has_fts(con):
            sql = ("SELECT p.note_id, p.heading, p.body, bm25(passages, 0, 4.0, 2.0, 1.0) AS s, n.title, n.status, n.confidence, "
                   "n.tier, n.updated, n.path, n.domain FROM passages p JOIN notes n ON n.id = p.note_id WHERE passages MATCH ? "
                   "ORDER BY s LIMIT 200")
            try:
                rows = con.execute(sql, (q,)).fetchall()
            except sqlite3.OperationalError:
                rows = []
        else:
            like = " OR ".join("(p.body LIKE ? OR p.title LIKE ?)" for _ in terms)
            params = [x for t in terms for x in (f"%{t}%", f"%{t}%")]
            rows = [(r[0], r[1], r[2], -1.0, *r[3:]) for r in con.execute(
                "SELECT p.note_id, p.heading, p.body, n.title, n.status, n.confidence, n.tier, n.updated, n.path, n.domain "
                f"FROM passages p JOIN notes n ON n.id=p.note_id WHERE {like} LIMIT 200", params)]
        if not include_rejected:
            rows = [r for r in rows if r[5] not in ("rejete",)]
        if domain:
            rows = [r for r in rows if r[10] == domain]
        # une étape plus large ne doit jamais effacer les résultats d'une étape plus précise
        if len({r[0] for r in rows}) > len({r[0] for r in best_rows}):
            best_rows, best_mode = rows, mode
        if len({r[0] for r in best_rows}) >= min(top_k, 2):
            break
    rows, mode_used = best_rows, best_mode
    con.close()
    scored = []
    for nid, heading, body, s, title, status, conf, tier, updated, path, dom in rows:
        relevance = -float(s) if s is not None else 0.0  # bm25() de SQLite : plus petit = meilleur
        w = STATUS_W.get(status, 0.8) * CONF_W.get(conf, 1.0) * TIER_W.get(int(tier or 4), 0.85) * _freshness(updated)
        scored.append((relevance * w, nid, heading, body, title, status, conf, tier, path, dom))
    scored.sort(key=lambda x: -x[0])
    results, used, per_note = [], 0, {}
    for sc, nid, heading, body, title, status, conf, tier, path, dom in scored:
        if per_note.get(nid, 0) >= 2:
            continue  # au plus 2 passages par fiche : favorise la diversité
        if len({r["note_id"] for r in results}) >= top_k and nid not in per_note:
            continue
        text = body if len(body) <= 700 else body[:700].rsplit(" ", 1)[0] + "…"
        header = f"[{nid}] {title} — {heading} ({status}, conf. {conf}, niv. {tier})"
        cost = approx_tokens(header + "\n" + text)
        if used + cost > token_budget:
            if not results:  # garantit au moins un passage, tronqué au budget
                room = max(60, int((token_budget - approx_tokens(header)) * 3.6) - 10)
                text = text[:room].rsplit(" ", 1)[0] + "…"
                cost = approx_tokens(header + "\n" + text)
            else:
                continue
        results.append({"note_id": nid, "title": title, "heading": heading, "text": text, "status": status,
                        "confidence": conf, "tier": tier, "path": path, "domain": dom, "score": round(sc, 4)})
        used += cost
        per_note[nid] = per_note.get(nid, 0) + 1
        if used >= token_budget:
            break
    return {"query": query, "mode": mode_used, "results": results, "tokens_estimated": used, "token_budget": token_budget,
            "hint": None if results else "Aucun passage : essayer des termes plus généraux ou get_topic_index(domaine)."}


def read_knowledge(note_id: str, token_budget: int = 3000, root: Path = ROOT) -> dict:
    con = connect(root)
    row = con.execute("SELECT path FROM notes WHERE id=?", (note_id,)).fetchone()
    con.close()
    if not row:
        return {"error": f"fiche inconnue : {note_id}"}
    path = (Path(root) / row[0]).resolve()
    if Path(root).resolve() / "knowledge" not in path.parents:
        return {"error": "chemin hors de la bibliothèque"}
    text = path.read_text(encoding="utf-8")
    meta, body = parse_note(text)
    limit = int(token_budget * 3.6)
    truncated = len(body) > limit
    return {"id": note_id, "path": row[0], "meta": {k: v for k, v in meta.items() if k not in ("tags",)},
            "body": body[:limit] + ("\n…[tronqué au budget]" if truncated else ""), "truncated": truncated}


def get_topic_index(topic: str, root: Path = ROOT, token_budget: int = 2500) -> dict:
    base = (Path(root) / "knowledge").resolve()
    name = re.sub(r"[^a-z0-9_-]", "", fold(topic))
    if not name or name in ("index", "general"):
        p = base / "_index.md"
    else:
        p = (base / name / "_index.md").resolve()
    if base not in p.parents and p != base / "_index.md":
        return {"error": "domaine invalide"}
    if not p.exists():
        domains = sorted(d.name for d in base.iterdir() if d.is_dir() and (d / "_index.md").exists())
        return {"error": f"pas d'index pour « {topic} »", "domains": domains}
    text = p.read_text(encoding="utf-8")
    limit = int(token_budget * 3.6)
    return {"topic": topic, "index": text[:limit] + ("\n…[tronqué]" if len(text) > limit else "")}
