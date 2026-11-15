"""V5.5 - etape 1 : decoupage structurel d'une source, sans perte d'ordre ni de contexte.

Ce module ne juge rien : il ne dit pas si une procedure est complete, ni si une
technique fonctionne. Il transforme une page (Markdown Roblox Docs, README GitHub,
texte brut) en blocs ordonnes, chacun rattache a son chemin de titres et a une
reference precise vers la source, pour que les extracteurs suivants puissent
citer exactement d'ou vient chaque instruction.

Garanties :
- l'ordre des blocs et des elements de liste est celui de la source ;
- le texte d'origine de chaque bloc est conserve dans ``raw`` ;
- le contenu des blocs de code n'est jamais modifie ;
- aucun texte n'est ajoute : ``text`` est seulement une version nettoyee de ``raw``.

Schema JSON stable : ``SCHEMA`` (voir ``to_dict``). Tout changement incompatible
doit incrementer la version du schema.
"""
from __future__ import annotations

import json
import re
import unicodedata

SCHEMA = "vdn.structure/1"

BLOCK_TYPES = ("heading", "paragraph", "list", "code", "table", "quote", "image")

# --------------------------------------------------------------------------- expressions
_FENCE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>`{3,}|~{3,})[ \t]*(?P<info>[^`]*?)[ \t]*$")
_ATX = re.compile(r"^[ ]{0,3}(?P<hashes>#{1,6})[ \t]+(?P<title>.*?)[ \t]*#*[ \t]*$")
_SETEXT = re.compile(r"^[ ]{0,3}(=+|-+)[ \t]*$")
_ITEM = re.compile(r"^(?P<indent>[ \t]*)(?:(?P<num>\d{1,9})[.)]|(?P<bullet>[-*+]))[ \t]+(?P<body>.*)$")
_TABLE_SEP = re.compile(r"^[ \t]*\|?[ \t]*:?-{2,}:?[ \t]*(\|[ \t]*:?-{2,}:?[ \t]*)*\|?[ \t]*$")
_QUOTE = re.compile(r"^[ ]{0,3}>[ ]?(?P<body>.*)$")
_IMAGE_ONLY = re.compile(r"^[ \t]*!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)[ \t]*$")
_HR = re.compile(r"^[ ]{0,3}([-*_])([ \t]*\1){2,}[ \t]*$")
_HTML_ONLY = re.compile(r"^[ \t]*<(?:/?[A-Za-z][\w.-]*)(?:\s[^>]*)?/?>[ \t]*$")
_HTML_COMMENT = re.compile(r"^[ \t]*<!--.*-->[ \t]*$")

# Reference Roblox dans les docs : `Class.SpotLight.Angle|Angle`, `Enum.Material.Snow`, ...
_API_KINDS = "Class|Enum|Datatype|Global|Library|Service"
_API_TICK = re.compile(r"`(?P<name>(?:" + _API_KINDS + r")\.[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*)(?:\|(?P<label>[^`]+))?`")
_API_BARE = re.compile(r"(?<![\w.`])(?P<name>(?:" + _API_KINDS + r")\.[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\|(?P<label>[A-Za-z_][\w.]*)")
_IMAGE_INLINE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_CODE_SPAN = re.compile(r"`([^`]+)`")
_EMPH = re.compile(r"(\*\*|__)(.+?)\1")
_CALLOUT = re.compile(r"^\*\*(?P<kind>info|note|tip|warning|caution|important|alert)\s*:?\*\*\s*:?\s*", re.I)


# --------------------------------------------------------------------------- nettoyage en ligne
def extract_api_refs(raw: str) -> list[dict]:
    """References d'API Roblox presentes dans un texte, dans l'ordre, sans doublon."""
    out, seen = [], set()
    for rx in (_API_TICK, _API_BARE):
        for m in rx.finditer(raw or ""):
            name = m.group("name")
            label = (m.group("label") or name.split(".")[-1]).strip()
            if (name, label) in seen:
                continue
            seen.add((name, label))
            out.append({"name": name, "label": label, "kind": name.split(".", 1)[0], "pos": m.start()})
    out.sort(key=lambda r: r["pos"])
    for r in out:
        del r["pos"]
    return out


def extract_links(raw: str) -> list[dict]:
    return [{"text": m.group(1), "url": m.group(2)} for m in _LINK.finditer(raw or "")]


def clean_inline(raw: str) -> str:
    """Texte lisible : references Roblox -> libelle, liens -> texte, sans marqueurs Markdown.

    Ne retire aucun mot de la source ; n'en ajoute aucun.
    """
    s = raw or ""
    s = _API_TICK.sub(lambda m: (m.group("label") or m.group("name").split(".")[-1]).strip(), s)
    s = _API_BARE.sub(lambda m: m.group("label"), s)
    s = _IMAGE_INLINE.sub(lambda m: m.group(1), s)
    s = _LINK.sub(lambda m: m.group(1), s)
    s = _CODE_SPAN.sub(lambda m: m.group(1), s)
    s = _EMPH.sub(lambda m: m.group(2), s)
    return re.sub(r"\s+", " ", s).strip()


def slug(title: str) -> str:
    """Ancre de titre a la maniere des docs Roblox / GitHub (``#shared-properties``)."""
    t = unicodedata.normalize("NFKD", clean_inline(title)).encode("ascii", "ignore").decode()
    t = re.sub(r"[^\w\s-]", "", t.lower()).strip()
    return re.sub(r"[\s_]+", "-", t)


# --------------------------------------------------------------------------- analyse
def _front_matter(lines: list[str]) -> tuple[dict, int]:
    if not lines or lines[0].strip() != "---":
        return {}, 0
    meta = {}
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            return meta, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", lines[i])
        if m:
            meta[m.group(1)] = m.group(2).strip().strip("'\"")
    return {}, 0


def _indent_width(s: str) -> int:
    return len(s.expandtabs(4)) - len(s.expandtabs(4).lstrip(" "))


class _Builder:
    def __init__(self, url: str):
        self.url = url
        self.blocks: list[dict] = []
        self.path: list[tuple[int, str, str]] = []  # (niveau, titre propre, ancre)

    def section(self) -> list[str]:
        return [t for _, t, _ in self.path]

    def anchor(self) -> str:
        return self.path[-1][2] if self.path else ""

    def ref(self, block_id: str, line: int, item: int | None = None) -> dict:
        a = self.anchor()
        r = {"url": f"{self.url}#{a}" if (self.url and a) else self.url, "section": " > ".join(self.section()),
             "block": block_id, "line": line}
        if item is not None:
            r["item"] = item
        return r

    def add(self, btype: str, raw: str, line_start: int, line_end: int, **extra) -> dict:
        bid = f"b{len(self.blocks):04d}"
        block = {"id": bid, "index": len(self.blocks), "type": btype,
                 "section": self.section(), "anchor": self.anchor(),
                 "line_start": line_start, "line_end": line_end,
                 "raw": raw, "text": extra.pop("text", clean_inline(raw) if btype != "code" else raw),
                 "api_refs": extra.pop("api_refs", extract_api_refs(raw) if btype != "code" else []),
                 "links": extract_links(raw) if btype != "code" else []}
        block.update(extra)
        block["ref"] = self.ref(bid, line_start)
        self.blocks.append(block)
        return block

    def heading(self, level: int, title_raw: str, line: int):
        title = clean_inline(title_raw)
        while self.path and self.path[-1][0] >= level:
            self.path.pop()
        self.path.append((level, title, slug(title_raw)))
        self.add("heading", title_raw, line, line, level=level)


def parse_markdown(text: str, url: str = "", provider: str = "", title: str = "") -> dict:
    """Decoupe un document Markdown en blocs ordonnes. Retourne le dict du schema ``SCHEMA``."""
    lines = (text or "").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    meta, i = _front_matter(lines)
    b = _Builder(url)
    n = len(lines)
    para: list[tuple[int, str]] = []

    def flush_para():
        if para:
            raw = "\n".join(s for _, s in para)
            b.add("paragraph", raw, para[0][0], para[-1][0])
            para.clear()

    while i < n:
        line = lines[i]
        ln = i + 1
        stripped = line.strip()

        if not stripped:
            flush_para(); i += 1; continue

        fm = _FENCE.match(line)
        if fm:
            flush_para()
            fence, indent = fm.group("fence"), _indent_width(fm.group("indent"))
            body, j = [], i + 1
            while j < n:
                close = _FENCE.match(lines[j])
                if close and close.group("fence")[0] == fence[0] and len(close.group("fence")) >= len(fence) and not close.group("info"):
                    break
                body.append(lines[j][indent:] if _indent_width(lines[j][:indent]) >= indent and lines[j][:indent].strip() == "" else lines[j])
                j += 1
            code = "\n".join(body)
            info = fm.group("info").strip()
            b.add("code", code, ln, min(j + 1, n), language=(info.split()[0].lower() if info else ""),
                  closed=j < n, **_list_context(b))
            i = j + 1
            continue

        if _HTML_COMMENT.match(line) or _HTML_ONLY.match(line):
            flush_para(); i += 1; continue

        m = _ATX.match(line)
        if m:
            flush_para(); b.heading(len(m.group("hashes")), m.group("title"), ln); i += 1; continue

        if para and _SETEXT.match(line) and not _ITEM.match(para[-1][1]):
            title_lines = list(para); para.clear()
            b.heading(1 if line.strip()[0] == "=" else 2, " ".join(s.strip() for _, s in title_lines), title_lines[0][0])
            i += 1; continue

        if _HR.match(line):
            flush_para(); i += 1; continue

        mi = _IMAGE_ONLY.match(line)
        if mi:
            flush_para()
            b.add("image", line.strip(), ln, ln, text=mi.group("alt").strip(), src=mi.group("src")); i += 1; continue

        if _QUOTE.match(line):
            flush_para()
            j, body = i, []
            while j < n and lines[j].strip() and _QUOTE.match(lines[j]):
                body.append(_QUOTE.match(lines[j]).group("body")); j += 1
            raw = "\n".join(body)
            cm = _CALLOUT.match(raw.strip())
            extra = {"callout": cm.group("kind").lower()} if cm else {}
            b.add("quote", raw, ln, j, text=clean_inline(_CALLOUT.sub("", raw.strip(), count=1)), **extra)
            i = j; continue

        if "|" in line and i + 1 < n and _TABLE_SEP.match(lines[i + 1]) and not para:
            j = i + 2
            while j < n and lines[j].strip() and "|" in lines[j]:
                j += 1
            raw_rows = lines[i:j]
            header = _cells(raw_rows[0])
            rows = [_cells(r) for r in raw_rows[2:]]
            b.add("table", "\n".join(raw_rows), ln, j,
                  text=" ; ".join(" | ".join(clean_inline(c) for c in r) for r in [header] + rows),
                  header=[clean_inline(c) for c in header], rows=[[clean_inline(c) for c in r] for r in rows])
            i = j; continue

        if _ITEM.match(line):
            flush_para()
            i = _parse_list(lines, i, b)
            continue

        para.append((ln, line.strip()))
        i += 1

    flush_para()
    _link_continued_lists(b.blocks)
    return _document(b.blocks, url, provider, title or meta.get("title", "") or _first_heading(b.blocks), "markdown", meta)


def _cells(row: str) -> list[str]:
    r = row.strip()
    if r.startswith("|"):
        r = r[1:]
    if r.endswith("|") and not r.endswith("\\|"):
        r = r[:-1]
    # Ne pas couper sur le | interne d'une reference `Class.X|Y` (entre accents graves).
    cells, buf, tick = [], "", False
    for ch in r:
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            cells.append(buf.strip()); buf = ""
        else:
            buf += ch
    cells.append(buf.strip())
    return cells


def _list_context(b: _Builder) -> dict:
    """Un bloc de code place juste apres un element de liste lui est rattache."""
    if b.blocks and b.blocks[-1]["type"] == "list" and b.blocks[-1]["section"] == b.section():
        last = b.blocks[-1]
        return {"after_list": last["id"], "after_item": last["items"][-1]["position"]}
    return {}


def _parse_list(lines: list[str], i: int, b: _Builder) -> int:
    """Lit une liste (et ses sous-listes) a partir de la ligne i. Retourne l'indice suivant."""
    n = len(lines)
    first = _ITEM.match(lines[i])
    base = _indent_width(first.group("indent"))
    ordered = first.group("num") is not None
    items, cur, j = [], None, i
    indents: list[int] = []

    while j < n:
        line = lines[j]
        if not line.strip():
            # Une ligne vide ne ferme la liste que si la suivante n'est ni un element ni une suite indentee.
            k = j + 1
            while k < n and not lines[k].strip():
                k += 1
            if k < n and (_ITEM.match(lines[k]) and _indent_width(_ITEM.match(lines[k]).group("indent")) >= base
                          and (_ITEM.match(lines[k]).group("num") is not None) == ordered
                          or _indent_width(lines[k]) > base and not _FENCE.match(lines[k])):
                j = k; continue
            break
        if _FENCE.match(line) or _ATX.match(line) or (_QUOTE.match(line) and _indent_width(line) <= base):
            break
        m = _ITEM.match(line)
        if m:
            ind = _indent_width(m.group("indent"))
            if ind < base:
                break
            if ind == base and (m.group("num") is not None) != ordered:
                break
            while indents and indents[-1] > ind:
                indents.pop()
            if not indents or indents[-1] < ind:
                indents.append(ind)
            depth = len(indents) - 1
            cur = {"position": len(items) + 1, "depth": depth,
                   "marker": m.group("num") + "." if m.group("num") else m.group("bullet"),
                   "number": int(m.group("num")) if m.group("num") else None,
                   "line": j + 1, "raw": m.group("body").strip()}
            items.append(cur)
        elif cur is not None:
            cur["raw"] += "\n" + line.strip()   # suite de l'element (continuation paresseuse)
        else:
            break
        j += 1

    top = [it for it in items if it["depth"] == 0]
    parent_stack: list[dict] = []
    for it in items:
        while parent_stack and parent_stack[-1]["depth"] >= it["depth"]:
            parent_stack.pop()
        it["parent"] = parent_stack[-1]["position"] if parent_stack else None
        parent_stack.append(it)
        it["text"] = clean_inline(it["raw"])
        it["api_refs"] = extract_api_refs(it["raw"])
        it["links"] = extract_links(it["raw"])
    block = b.add("list", "\n".join(lines[i:j]).rstrip(), i + 1, j,
                  text=" ".join(it["text"] for it in items), api_refs=extract_api_refs("\n".join(it["raw"] for it in items)),
                  ordered=ordered, start=(top[0]["number"] if ordered and top and top[0]["number"] is not None else None),
                  items=items)
    for it in items:
        it["ref"] = b.ref(block["id"], it["line"], it["position"])
    return j


def _link_continued_lists(blocks: list[dict]):
    """Liste numerotee reprise apres un bloc de code (3. apres 1., 2., code) : on note la continuite.

    Seul le numero ecrit dans la source est utilise ; rien n'est renumerote.
    """
    last_ordered: dict | None = None
    for blk in blocks:
        if blk["type"] == "heading":
            last_ordered = None
            continue
        if blk["type"] != "list" or not blk.get("ordered"):
            continue
        if last_ordered is not None and blk["section"] == last_ordered["section"] and blk.get("start"):
            prev_nums = [it["number"] for it in last_ordered["items"] if it["depth"] == 0 and it["number"] is not None]
            if prev_nums and blk["start"] == prev_nums[-1] + 1:
                blk["continues"] = last_ordered["id"]
        last_ordered = blk


def _first_heading(blocks: list[dict]) -> str:
    return next((x["text"] for x in blocks if x["type"] == "heading"), "")


def _document(blocks: list[dict], url: str, provider: str, title: str, fmt: str, meta: dict | None = None) -> dict:
    counts = {t: 0 for t in BLOCK_TYPES}
    for x in blocks:
        counts[x["type"]] = counts.get(x["type"], 0) + 1
    return {
        "schema": SCHEMA,
        "source": {"url": url, "provider": provider, "format": fmt, "title": clean_inline(title)},
        "meta": meta or {},
        "blocks": blocks,
        "stats": {"blocks": len(blocks), "by_type": counts,
                  "ordered_lists": sum(1 for x in blocks if x["type"] == "list" and x.get("ordered")),
                  "list_items": sum(len(x.get("items", [])) for x in blocks),
                  "api_refs": sum(len(x["api_refs"]) for x in blocks)},
    }


def parse_text(text: str, url: str = "", provider: str = "", title: str = "") -> dict:
    """Texte brut (ex. message de forum deja nettoye) : paragraphes separes par des lignes vides.

    Les listes numerotees ecrites en texte brut sont reconnues comme en Markdown.
    """
    doc = parse_markdown(text or "", url=url, provider=provider, title=title)
    doc["source"]["format"] = "text"
    return doc


def parse(text: str, url: str = "", provider: str = "", title: str = "") -> dict:
    """Point d'entree unique ; le format est deduit du fournisseur."""
    if provider in ("roblox_docs", "github"):
        return parse_markdown(text, url=url, provider=provider, title=title)
    return parse_text(text, url=url, provider=provider, title=title)


# --------------------------------------------------------------------------- utilitaires
def to_json(doc: dict) -> str:
    return json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=False)


def from_json(raw: str) -> dict:
    doc = json.loads(raw)
    if doc.get("schema") != SCHEMA:
        raise ValueError(f"schema inattendu : {doc.get('schema')!r} (attendu {SCHEMA})")
    return doc


def section_blocks(doc: dict, *titles: str) -> list[dict]:
    """Blocs dont le chemin de titres contient, dans l'ordre, les titres donnes (insensible a la casse)."""
    want = [t.lower() for t in titles]
    out = []
    for blk in doc["blocks"]:
        path = [s.lower() for s in blk["section"]]
        k = 0
        for p in path:
            if k < len(want) and p == want[k]:
                k += 1
        if k == len(want):
            out.append(blk)
    return out


def sequence(doc: dict, list_id: str) -> list[dict]:
    """Elements de premier niveau d'une liste numerotee et de ses reprises, dans l'ordre de la source."""
    by_id = {x["id"]: x for x in doc["blocks"]}
    chain = [by_id[list_id]]
    for blk in doc["blocks"]:
        if blk.get("continues") == chain[-1]["id"]:
            chain.append(blk)
    return [it for blk in chain for it in blk["items"] if it["depth"] == 0]
