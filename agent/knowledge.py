"""Bibliothèque Markdown compatible Obsidian : une fiche par technique, statuts honnêtes, index par domaine.

Règles inviolables :
- Une fiche n'est JAMAIS « validée » automatiquement : seuls des tests réels dans Roblox Studio (saisis par un humain
  ou par Claude après test) peuvent passer une fiche en « reproduit » ou « validé pour le jeu ».
- Aucune fiche existante n'est supprimée : une ancienne fiche hors sujet passe au statut « rejeté », avec la raison.
- Les chiffres et paramètres ne sont recopiés que s'ils figurent dans un extrait de la source citée.
"""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

from agent.text import fold, tokens
from agent.providers import canonical_url
from agent.procedure import actionable_excerpts

ROOT = Path(__file__).resolve().parents[1]
STATUSES = ["candidat", "documente", "reproduit", "valide", "rejete", "obsolete"]
STATUS_LABEL = {"candidat": "Candidat", "documente": "Documenté", "reproduit": "Reproduit dans Studio",
                "valide": "Validé pour le jeu", "rejete": "Rejeté", "obsolete": "Obsolète"}
STATUS_RANK = {"valide": 0, "reproduit": 1, "documente": 2, "candidat": 3, "obsolete": 4, "rejete": 5}
CONF_RANK = {"haute": 0, "moyenne": 1, "faible": 2}
LEGACY_DOMAIN = {"spruce": ("vegetation", "spruce"), "forest": ("forest", "forest"), "character": ("characters", "character"),
                 "manor": ("architecture", "manor"), "traversal": ("animation", "traversal")}
SECTIONS = ["Objectif", "Description technique", "Étapes reproductibles", "Paramètres (sourcés)", "Limites connues de Roblox",
            "Extraits justificatifs", "Problèmes connus", "Alternatives", "Tests dans Roblox Studio", "Questions ouvertes"]


def relevance_threshold() -> float:
    from agent.relevance import ACCEPT
    return ACCEPT["topical"]


def today() -> str:
    return dt.date.today().isoformat()


def note_id(canonical: str) -> str:
    return "vdn-" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]


def slugify(value: str, n: int = 60) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", fold(value)).strip("-")
    return s[:n].strip("-") or "fiche"


# ------------------------------------------------------------------ frontmatter (sous-ensemble YAML lisible par Obsidian)
def dump_frontmatter(meta: dict) -> str:
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            lines += [f"  - {json.dumps(str(x), ensure_ascii=False)}" for x in v]
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, (int, float)):
            lines.append(f"{k}: {v}")
        else:
            lines.append(f"{k}: {json.dumps(str(v), ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _scalar(raw: str):
    raw = raw.strip()
    if not raw:
        return ""
    if raw[0] in "\"'[{" or raw in ("true", "false", "null") or re.fullmatch(r"-?\d+(\.\d+)?", raw):
        try:
            return json.loads(raw if raw[0] != "'" else '"' + raw[1:-1].replace('"', '\\"') + '"')
        except ValueError:
            pass
    return raw


def parse_note(text: str) -> tuple[dict, str]:
    """Sépare le frontmatter et le corps. Tolérant : un fichier sans frontmatter donne ({}, texte)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    meta, key = {}, None
    for line in text[3:end].strip("\n").splitlines():
        if re.match(r"^\s+-\s", line) and key:
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(_scalar(line.split("-", 1)[1]))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            meta[key] = _scalar(m.group(2)) if m.group(2).strip() else []
    body = text[end + 4:]
    return meta, body.lstrip("\n")


def sections(body: str) -> dict[str, str]:
    out, current, buf = {}, "_intro", []
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            out[current] = "\n".join(buf).strip()
            current, buf = m.group(1), []
        else:
            buf.append(line)
    out[current] = "\n".join(buf).strip()
    return out


# ------------------------------------------------------------------ registre (déduplication par URL canonique)
class Registry:
    def __init__(self, root: Path = ROOT):
        self.root = Path(root)
        self.path = self.root / "output" / "registry.json"
        data = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        self.urls: dict = data.get("urls", {})
        self.fingerprints: dict = data.get("fingerprints", {})

    def find(self, url: str):
        return self.urls.get(canonical_url(url))

    def add(self, url: str, nid: str, path: Path):
        self.urls[canonical_url(url)] = {"id": nid, "path": str(Path(path).relative_to(self.root)).replace("\\", "/")}

    def excerpt_seen(self, excerpt: str, nid: str) -> bool:
        """Vrai si le même extrait figure déjà dans une AUTRE fiche (doublon de contenu, ex. dépôt copié)."""
        fp = hashlib.sha256(" ".join(tokens(excerpt, keep_stop=True)).encode()).hexdigest()[:16]
        owner = self.fingerprints.get(fp)
        if owner and owner != nid:
            return True
        self.fingerprints[fp] = nid
        return False

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"urls": self.urls, "fingerprints": self.fingerprints}, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(self.path)


# ------------------------------------------------------------------ règles de statut et de confiance
def decide_status(assessment: dict, tier: int, official: bool) -> tuple[str, str, str]:
    """Retourne (statut, confiance, justification). Jamais « reproduit » ni « validé » ici."""
    n = len(assessment.get("excerpts", []))
    if not assessment.get("accepted"):
        return "rejete", "faible", "; ".join(assessment.get("reasons", []))
    steps = actionable_excerpts(assessment.get("excerpts", []))
    if n >= 2 and steps and (tier <= 2 or official):
        conf = "moyenne" if (tier == 1 or official) and n >= 3 else "faible"
        why = (f"{n} passages techniques dont {len(steps)} avec action et objet identifiables, source de niveau {tier}"
               + (" (réponse du personnel Roblox / doc officielle)" if official else "")
               + " ; indice technique seulement, procédure complète non garantie ; aucun test dans Roblox Studio.")
        return "documente", conf, why
    return "candidat", "faible", f"{n} passage(s) technique(s), {len(steps)} instruction(s) explicite(s) repérée(s), source de niveau {tier} ; procédure à approfondir et à tester."


_PARAM = re.compile(r"(?i)(\b\d+(?:[.,]\d+)?\s*(?:px|k|kb|mb|studs?|tris|triangles?|vertices|bones?|%|°)\b|\b[A-Z][a-zA-Z]+\s*=\s*[\w.\"]+|"
                    r"\b(?:AlphaMode|RenderFidelity|CollisionFidelity|ColorMap|NormalMap|RoughnessMap|MetalnessMap|"
                    r"Density|Haze|Glare|Brightness|ExposureCompensation|ShadowSoftness|Technology|StreamingEnabled|"
                    r"LevelOfDetail|ModelStreamingMode|DoubleSided|TextureContent|MaterialVariant)\b)")
_LIMIT = re.compile(r"(?i)\b(cannot|can't|can not|not supported|unsupported|only|limit|limited|maximum|max|at most|does not|doesn't|won't|bug|issue)\b")


def build_body(title: str, query: str, topic: dict, assessment: dict, src: dict, accessed: str, status: str) -> str:
    ex = assessment.get("excerpts", [])
    params = [e for e in ex if _PARAM.search(e)]
    limits = [e for e in ex if _LIMIT.search(e)]
    link = f"[{src.get('provider_label', src['provider'])}]({src['url']})"
    lines = [f"# {title}", "",
             f"> **{STATUS_LABEL[status]}** · source {link} · consultée le {accessed} · **non testée dans Roblox Studio**", "",
             "## Objectif", "", f"Répondre à : *{query}* (sujet : {topic.get('title', topic.get('id'))}).", "",
             "## Description technique", "", "À rédiger à partir des extraits ci-dessous (analyse humaine ou Ollama). "
             "Rien n'est affirmé ici sans source.", "",
             "## Étapes reproductibles", "", "Instructions extraites automatiquement : procedure partielle, ordre et fonctionnement non verifies.", ""]
    steps = actionable_excerpts(ex)
    lines += [f"{i}. {e} -- {link}" for i, e in enumerate(steps, 1)] or [
        "Aucune instruction complete identifiee. Consulter la source."
    ]
    lines += ["", "## Paramètres (sourcés)", ""]
    lines += [f"- « {p} » — {link}" for p in params] or ["Aucun paramètre chiffré trouvé dans les extraits."]
    lines += ["", "## Limites connues de Roblox", ""]
    lines += [f"- « {l} » — {link}" for l in limits] or ["Aucune limite explicite trouvée dans les extraits."]
    lines += ["", "## Extraits justificatifs", ""]
    lines += [f"> « {e} »\n> — {link}, consulté le {accessed}\n" for e in ex] or ["Aucun extrait technique."]
    lines += ["", "## Problèmes connus", "", "À compléter.", "", "## Alternatives", "", "À compléter.", "",
              "## Tests dans Roblox Studio", "", "- Testé : **non**", "- Conditions : —", "- Résultat : —", "",
              "## Questions ouvertes", ""]
    qs = []
    if not params:
        qs.append(f"Quels réglages exacts (valeurs, propriétés) pour « {query} » ?")
    if not limits:
        qs.append(f"Quelles limites Roblox (performances, rendu à distance, appareils) pour « {query} » ?")
    qs.append("Le résultat tient-il de nuit, à la lampe torche, sur mobile ?")
    lines += [f"- {q}" for q in qs]
    lines += ["", "## Scores (diagnostic, pas une preuve)", "",
              f"- Pertinence sujet : {assessment.get('topical')} · Contenu technique : {assessment.get('technical')} · "
              f"Lien Roblox : {'oui' if assessment.get('roblox') else 'non'}",
              f"- Termes techniques repérés : {', '.join(assessment.get('tech_terms', [])) or '—'}", ""]
    return "\n".join(lines)


def write_note(root: Path, registry: Registry, topic: dict, query: str, src: dict, doc: dict, assessment: dict) -> dict:
    """Crée ou met à jour la fiche d'une source. Retourne {'action': created|updated|duplicate, 'id', 'path', 'status'}."""
    root = Path(root)
    canon = canonical_url(src["url"])
    existing = registry.find(canon)
    accessed = today()
    if existing:
        path = root / existing["path"]
        if path.exists():
            meta, body = parse_note(path.read_text(encoding="utf-8"))
            qs = meta.get("queries") if isinstance(meta.get("queries"), list) else []
            if query not in qs:
                meta["queries"] = qs + [query]
                meta["updated"] = accessed
                path.write_text(dump_frontmatter(meta) + "\n" + body, encoding="utf-8")
                return {"action": "updated", "id": existing["id"], "path": existing["path"], "status": meta.get("status")}
        return {"action": "duplicate", "id": existing["id"], "path": existing["path"], "status": None}
    nid = note_id(canon)
    # doublons de contenu : on retire les extraits déjà présents dans une autre fiche
    unique = [e for e in assessment.get("excerpts", []) if not registry.excerpt_seen(e, nid)]
    dup_excerpts = len(assessment.get("excerpts", [])) - len(unique)
    assessment = {**assessment, "excerpts": unique}
    status, conf, why = decide_status(assessment, src.get("tier", 4), doc.get("official", False))
    if status == "rejete":
        return {"action": "rejected", "id": nid, "path": None, "status": status, "reasons": assessment.get("reasons")}
    domain = topic.get("domain", topic["id"])
    title = re.sub(r"\s+", " ", doc.get("title") or src.get("title") or canon).strip()[:160]
    meta = {"id": nid, "title": title, "domain": domain, "subdomain": topic["id"], "status": status,
            "tested_in_studio": "non", "confidence": conf, "confidence_reason": why,
            "engine_version": "inconnue", "source_tier": src.get("tier", 4), "provider": src["provider"],
            "official": bool(doc.get("official")), "sources": [canon], "accessed": accessed,
            "queries": [query], "created": accessed, "updated": accessed,
            "tags": ["vdn", domain, topic["id"], status]}
    for k in ("staff_posts", "accepted_answer", "stars", "pushed", "license", "last_posted"):
        if doc.get("meta", {}).get(k) not in (None, ""):
            meta[k] = doc["meta"][k]
    if dup_excerpts:
        meta["duplicate_excerpts"] = dup_excerpts
    folder = root / "knowledge" / domain
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{nid[4:]}-{slugify(title, 50)}.md"
    src = {**src, "provider_label": {"roblox_docs": "Documentation Roblox", "devforum": "Roblox DevForum",
                                     "github": "GitHub", "searxng": "Web"}.get(src["provider"], src["provider"])}
    path.write_text(dump_frontmatter(meta) + "\n" + build_body(title, query, topic, assessment, src, accessed, status), encoding="utf-8")
    registry.add(canon, nid, path)
    return {"action": "created", "id": nid, "path": str(path.relative_to(root)).replace("\\", "/"), "status": status}


# ------------------------------------------------------------------ migration des fiches V1–V4 (aucune suppression)
def legacy_evidence(body: str) -> str:
    """Texte de la SOURCE d'une ancienne fiche : extrait de découverte + passages repérés par V2/V3.
    Ne jamais inclure les lignes « Question de recherche » / « Sujet » écrites par l'agent : elles contiennent la
    requête elle-même et rendaient toute fiche « pertinente » à 100 % (bug trouvé pendant la migration V5)."""
    secs = sections(body)
    parts = [secs.get("Extrait de découverte (non vérifié)", "")]
    for name, txt in secs.items():
        if name.startswith(("Analyse V2", "Analyse V3")):
            parts.append(txt)
    evidence = "\n".join(p for p in parts if p)
    evidence = re.sub(r"(?m)^\s*\*\*(Statut|Source lue|Contenu|Contenu accessible|Passages candidats)\s*:\*\*.*$", "", evidence)
    evidence = re.sub(r"(?ms)^###?\s*(Questions|Validation|Limites et validation).*?(?=^###|\Z)", "", evidence)
    return evidence.strip()


def migrate_legacy(root: Path = ROOT, assess_fn=None) -> dict:
    """Ajoute le nouveau frontmatter aux anciennes fiches, sans toucher à leur contenu historique.
    Classe chaque ancienne fiche (candidat / documenté / rejeté + raison) avec le nouveau filtre de pertinence,
    appliqué au titre, à l'extrait et aux passages V3 déjà présents dans la fiche."""
    from agent import relevance
    assess_fn = assess_fn or relevance.assess
    root = Path(root)
    cfg = json.loads((root / "config" / "topics.json").read_text(encoding="utf-8"))
    topics = {t["id"]: t for t in cfg["topics"]}
    reg = Registry(root)
    report = {"migrated": 0, "already": 0, "by_status": {}}
    for path in sorted((root / "knowledge").glob("*/*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        meta, body = parse_note(text)
        if meta.get("id"):
            report["already"] += 1
            continue
        m = re.search(r"\*\*Source :\*\* \[([^\]]+)\]\((https://[^)]+)\)", body)
        url = m.group(2) if m else ""
        provider = "devforum" if "devforum.roblox.com" in url else "github" if "github.com" in url else "inconnu"
        tier = {"devforum": 2, "github": 3}.get(provider, 4)
        title_m = re.search(r"^#\s+(.+)$", body, re.M)
        title = (title_m.group(1).strip() if title_m else path.stem).replace("\\[", "[").replace("\\]", "]")
        q_m = re.search(r"\*\*Question de recherche :\*\*\s*(.+)", body)
        query = q_m.group(1).strip() if q_m else title
        topic_id = str(meta.get("topic") or path.parent.name)
        topic = topics.get(topic_id, {"id": topic_id, "title": topic_id})
        evidence = legacy_evidence(body)
        a = assess_fn(query, title, evidence, provider=provider)
        status, conf, why = decide_status(a, tier, False)
        # Une ancienne fiche n'a souvent qu'un court extrait : « pas assez de contenu technique » ne prouve pas qu'elle
        # est hors sujet. Si c'est la SEULE raison et que le sujet correspond, elle reste candidate (« à relire »).
        if status == "rejete" and a["topical"] >= relevance_threshold() and a["roblox"] and not a["noise"]:
            status, conf, why = "candidat", "faible", "extrait trop court pour juger ; source à relire en entier"
        domain, sub = LEGACY_DOMAIN.get(topic_id, (topic.get("domain", topic_id), topic_id))
        canon = canonical_url(url) if url else ""
        nid = note_id(canon or str(path))
        new_meta = {"id": nid, "title": title[:160], "domain": domain, "subdomain": sub, "status": status,
                    "tested_in_studio": "non", "confidence": conf,
                    "confidence_reason": ("Ancienne fiche V1–V4 reclassée automatiquement : " + why),
                    "engine_version": "inconnue", "source_tier": tier, "provider": provider, "official": False,
                    "sources": [canon] if canon else [], "accessed": str(meta.get("collected_utc", ""))[:10],
                    "queries": [query], "created": str(meta.get("collected_utc", ""))[:10] or today(), "updated": today(),
                    "tags": ["vdn", domain, sub, status, "migre-v5"]}
        # aucune donnée perdue : chaque ancien champ est recopié tel quel sous le préfixe legacy_
        for k, v in meta.items():
            new_meta["legacy_" + re.sub(r"[^a-z0-9_]", "_", str(k).lower())] = v
        if status == "rejete":
            new_meta["rejection_reason"] = "; ".join(a.get("reasons", []))
        banner = (f"> **{STATUS_LABEL[status]}** (reclassement V5 du {today()}) · {why}\n"
                  "> Le contenu historique ci-dessous est conservé tel quel.\n\n")
        path.write_text(dump_frontmatter(new_meta) + "\n" + banner + body, encoding="utf-8")
        if canon:
            reg.add(canon, nid, path)
        report["migrated"] += 1
        report["by_status"][status] = report["by_status"].get(status, 0) + 1
    reg.save()
    return report


# ------------------------------------------------------------------ index Obsidian (général + par domaine)
def load_notes(root: Path = ROOT) -> list[dict]:
    out = []
    for path in sorted((Path(root) / "knowledge").rglob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_note(path.read_text(encoding="utf-8"))
        if not meta.get("id"):
            continue
        meta["_path"] = str(path.relative_to(root)).replace("\\", "/")
        meta["_body"] = body
        out.append(meta)
    return out


def summary_line(meta: dict) -> str:
    body = meta.get("_body", "")
    ex = re.search(r"^>\s*«\s*(.+?)\s*»\s*$", body, re.M)
    s = ex.group(1) if ex else ""
    return (s[:140] + "…") if len(s) > 140 else s


def build_indexes(root: Path = ROOT) -> dict:
    root = Path(root)
    notes = load_notes(root)
    by_domain: dict[str, list] = {}
    for n in notes:
        by_domain.setdefault(str(n.get("domain", "divers")), []).append(n)

    def sort_key(n):
        return (STATUS_RANK.get(n.get("status"), 9), CONF_RANK.get(n.get("confidence"), 9), int(n.get("source_tier", 9) or 9), n.get("title", ""))

    def link(n):
        rel = Path(n["_path"]).relative_to("knowledge").with_suffix("").as_posix()
        return f"[[{rel}|{n.get('title', n['id'])}]]"

    stats = {}
    general = ["# Bibliothèque VDN — index général", "",
               "Une fiche = une source/technique. Statuts : candidat → documenté → reproduit → validé. "
               "Aucune fiche n'est validée sans test réel dans Roblox Studio.", "",
               "| Domaine | Validées | Reproduites | Documentées | Candidates | Rejetées |", "|---|---:|---:|---:|---:|---:|"]
    for domain in sorted(by_domain):
        items = sorted(by_domain[domain], key=sort_key)
        c = {s: sum(1 for n in items if n.get("status") == s) for s in STATUSES}
        stats[domain] = c
        general.append(f"| [[{domain}/_index|{domain}]] | {c['valide']} | {c['reproduit']} | {c['documente']} | {c['candidat']} | {c['rejete']} |")
        lines = [f"# Index — {domain}", "",
                 "Classement : statut, puis confiance, puis niveau de la source (1 = doc officielle). "
                 "Les fiches rejetées sont en bas, gardées pour l'historique.", ""]
        for status in ["valide", "reproduit", "documente", "candidat"]:
            group = [n for n in items if n.get("status") == status]
            if not group:
                continue
            lines += [f"## {STATUS_LABEL[status]} ({len(group)})", ""]
            for n in group:
                tag = f"niv. {n.get('source_tier', '?')} · conf. {n.get('confidence', '?')}"
                s = summary_line(n)
                lines.append(f"- {link(n)} — {tag}" + (f" — « {s} »" if s else ""))
            lines.append("")
        rej = [n for n in items if n.get("status") in ("rejete", "obsolete")]
        if rej:
            lines += [f"## Rejetées / obsolètes ({len(rej)})", ""]
            lines += [f"- {link(n)} — {n.get('rejection_reason', n.get('confidence_reason', ''))[:120]}" for n in rej]
            lines.append("")
        d = root / "knowledge" / domain
        d.mkdir(parents=True, exist_ok=True)
        (d / "_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    general += ["", f"Total : {len(notes)} fiches. Mis à jour le {today()}.", ""]
    (root / "knowledge" / "_index.md").write_text("\n".join(general), encoding="utf-8")
    return stats
