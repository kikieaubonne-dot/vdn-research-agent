"""Fournisseurs de sources, gratuits, respectant les règles de chaque site. Bibliothèque standard uniquement.

Le contenu récupéré est une DONNÉE non fiable : il n'est jamais exécuté ni suivi comme une instruction.

Niveaux de confiance a priori des sources (tier) :
  1 = documentation officielle Roblox ; 2 = DevForum (réponse du personnel Roblox = 1) ; 3 = GitHub ; 4 = web via SearXNG.
Un tier élevé ne prouve rien : chaque affirmation reste à vérifier.

Corrections V4.1 :
- DevForum : la recherche /search.json est INTERDITE aux robots (robots.txt du DevForum, vérifié le 15-11-2026).
  On découvre les sujets par le sitemap (autorisé) et on lit /t/<id>.json (autorisé).
- GitHub : requêtes courtes (3-4 termes) ; la recherche GitHub combine les mots en ET, les requêtes V3 de 6-7 mots
  ne renvoyaient presque rien (reproduit : 1 seul dépôt sans description pour la requête « forest … troubleshooting »).
"""
from __future__ import annotations
import gzip
import json
import os
import re
import time
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlunparse
from urllib.request import Request, urlopen

from agent.text import BM25, tokens, fold, vocabulary, stem

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "VDNResearchAgent/5.0 (+https://github.com/kikieaubonne-dot/vdn-research-agent; non-commercial research)"
MAX_BYTES = 3_000_000
ALLOWED_HOSTS = {"create.roblox.com", "devforum.roblox.com", "api.github.com", "raw.githubusercontent.com", "github.com"}
DOCS_INDEX_URL = "https://create.roblox.com/docs/llms.txt"
DEVFORUM_SITEMAP = "https://devforum.roblox.com/sitemap.xml"
# Chemins DevForum que l'agent s'autorise (tout le reste est refusé, recherche et RSS compris).
DEVFORUM_ALLOWED = re.compile(r"^/(t/[^/]+/\d+(?:\.json)?|t/\d+\.json|sitemap[^/]*\.xml)$")


class FetchError(Exception):
    pass


def canonical_url(url: str) -> str:
    """URL canonique pour la déduplication : https, hôte en minuscules, sans suivi ni ancre, sans « / » final."""
    p = urlparse(url.strip())
    host = (p.hostname or "").lower()
    path = re.sub(r"/+$", "", p.path) or "/"
    if host == "devforum.roblox.com":
        m = re.match(r"^/t/(?:[^/]+/)?(\d+)", path)
        if m:
            return f"https://devforum.roblox.com/t/{m.group(1)}"
    if host == "github.com":
        m = re.match(r"^/([^/]+)/([^/]+)", path)
        if m:
            return f"https://github.com/{m.group(1).lower()}/{m.group(2).lower().removesuffix('.git')}"
    if host == "create.roblox.com":
        path = re.sub(r"^/docs/(?:[a-z]{2}-[a-z]{2}/)?", "/docs/", path).removesuffix(".md")
    return urlunparse(("https", host, path, "", "", ""))


def http_get(url: str, accept: str = "*/*", max_bytes: int = MAX_BYTES, retries: int = 2, extra_headers=None,
             allow_extra_hosts=()) -> str:
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if p.scheme != "https" or host not in ALLOWED_HOSTS | set(allow_extra_hosts):
        raise FetchError(f"hôte non autorisé : {host}")
    if host == "devforum.roblox.com" and not DEVFORUM_ALLOWED.match(p.path):
        raise FetchError(f"chemin DevForum non autorisé (robots.txt) : {p.path}")
    headers = {"User-Agent": USER_AGENT, "Accept": accept}
    if host == "api.github.com" and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    headers.update(extra_headers or {})
    last = None
    for attempt in range(retries + 1):
        try:
            with urlopen(Request(url, headers=headers), timeout=20) as r:
                final = (urlparse(r.geturl()).hostname or "").lower()
                if final not in ALLOWED_HOSTS | set(allow_extra_hosts):
                    raise FetchError(f"redirection hors liste : {final}")
                raw = r.read(max_bytes + 1)
                if len(raw) > max_bytes:
                    raise FetchError("réponse trop grande")
                if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                    raw = gzip.decompress(raw)
                return raw.decode("utf-8", "replace")
        except HTTPError as e:
            last = e
            if e.code in (429, 502, 503, 504) and attempt < retries:
                wait = int(e.headers.get("Retry-After", "0") or 0) or 3 * (attempt + 1)
                time.sleep(min(wait, 30))
                continue
            raise FetchError(f"HTTP {e.code} sur {host}") from e
        except (URLError, TimeoutError) as e:
            last = e
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
                continue
            raise FetchError(f"réseau : {type(e).__name__} sur {host}") from e
    raise FetchError(str(last))


class _Plain(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        if tag in ("p", "li", "br", "h1", "h2", "h3", "h4", "pre", "tr", "blockquote"):
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def strip_html(value: str) -> str:
    p = _Plain()
    p.feed(str(value or ""))
    text = "".join(p.parts)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()


def _cache_dir(root: Path) -> Path:
    d = Path(root) / "output" / "cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------- Documentation officielle Roblox (tier 1)
_LINK = re.compile(r"\[([^\]]+)\]\((\S+?\.md)\)(?::\s*(.*))?")


def parse_llms_index(text: str) -> list[dict]:
    """Analyse llms.txt : liste de liens .md regroupés sous des titres « ## Section »."""
    entries, section = [], ""
    for line in text.splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip()
            continue
        for m in _LINK.finditer(line):
            title, href, desc = m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()
            if href.startswith("/"):
                href = "https://create.roblox.com" + href
            if not href.startswith("https://create.roblox.com/docs"):
                continue
            entries.append({"title": title, "url": href, "section": section, "description": desc[:300]})
    seen, out = set(), []
    for e in entries:
        if e["url"] not in seen:
            seen.add(e["url"])
            out.append(e)
    return out


class RobloxDocs:
    name, tier = "roblox_docs", 1

    def __init__(self, root: Path = ROOT, getter=http_get):
        self.root, self.get = Path(root), getter
        self.path = _cache_dir(root) / "roblox_docs_index.json"
        self._bm25 = None
        self._entries = None

    def refresh(self) -> int:
        entries = parse_llms_index(self.get(DOCS_INDEX_URL, accept="text/markdown,text/plain"))
        if len(entries) < 50:
            raise FetchError(f"index officiel suspect ({len(entries)} entrées) : cache conservé")
        self.path.write_text(json.dumps({"fetched": int(time.time()), "entries": entries}, ensure_ascii=False), encoding="utf-8")
        self._entries = None
        return len(entries)

    def entries(self) -> list[dict]:
        if self._entries is None:
            self._entries = json.loads(self.path.read_text(encoding="utf-8"))["entries"] if self.path.exists() else []
            docs = [tokens(f"{e['title']} {e['title']} {e['section']} {e['url'].rsplit('/docs/', 1)[-1]} {e['description']}") for e in self._entries]
            self._bm25 = BM25(docs)
        return self._entries

    def search(self, query: str, limit: int = 5) -> list[dict]:
        entries = self.entries()
        if not entries:
            return []
        hits = self._bm25.top(tokens(query), k=limit, min_score=0.5)
        return [{"url": entries[i]["url"], "title": entries[i]["title"], "snippet": entries[i]["description"] or entries[i]["section"],
                 "provider": self.name, "tier": self.tier, "rank_score": round(s, 3)} for i, s in hits]

    def fetch(self, url: str) -> dict:
        if not url.endswith(".md"):
            url = url.rstrip("/") + ".md"
        text = self.get(url, accept="text/markdown,text/plain")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        return {"title": m.group(1).strip() if m else url.rsplit("/", 1)[-1], "text": text[:60000],
                "official": True, "meta": {"kind": "documentation officielle"}}


# ---------------------------------------------------------------- DevForum (tier 2, staff = 1)
def _slug_is_relevant(slug: str) -> bool:
    voc = vocabulary()
    words = set(stem(w) for w in fold(slug).split("-") if w)
    idx = voc["_syn_index"]
    tech = {stem(fold(t)) for t in voc.get("tech", []) if " " not in t}
    return bool(words & (set(idx) | tech))


class DevForum:
    name, tier = "devforum", 2

    def __init__(self, root: Path = ROOT, getter=http_get, pause: float = 1.5):
        self.root, self.get, self.pause = Path(root), getter, pause
        self.index_path = _cache_dir(root) / "devforum_index.json"
        self.progress_path = _cache_dir(root) / "devforum_sitemaps.json"
        self._bm25 = None
        self._topics = None

    def _load(self, path, default):
        try:
            return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default
        except ValueError:
            return default

    def refresh(self, max_pages: int = 3) -> dict:
        """Lit au plus max_pages pages de sitemap par appel (reprise au prochain lancement). Garde les sujets
        dont le titre contient un terme du domaine (le reste du forum ne nous concerne pas)."""
        prog = self._load(self.progress_path, {"pending": [], "done": [], "listed": 0})
        if not prog["pending"] or time.time() - prog.get("listed", 0) > 7 * 86400:
            root_xml = self.get(DEVFORUM_SITEMAP, accept="application/xml")
            locs = [l for l in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", root_xml) if "sitemap" in l]
            recent = [l for l in locs if "recent" in l]
            prog["pending"] = recent + [l for l in locs if l not in recent and l not in prog.get("done", [])]
            prog["listed"] = time.time()
        topics = {t["id"]: t for t in self._load(self.index_path, {"topics": []}).get("topics", [])}
        read = 0
        while prog["pending"] and read < max_pages:
            url = prog["pending"].pop(0)
            xml = self.get(url, accept="application/xml")
            for loc, lastmod in re.findall(r"<loc>\s*([^<]+?)\s*</loc>(?:\s*<lastmod>\s*([^<]+?)\s*</lastmod>)?", xml):
                m = re.match(r"https://devforum\.roblox\.com/t/([^/]+)/(\d+)", loc)
                if m and _slug_is_relevant(m.group(1)):
                    topics[int(m.group(2))] = {"id": int(m.group(2)), "slug": m.group(1), "lastmod": lastmod[:10]}
            if "recent" not in url:
                prog.setdefault("done", []).append(url)
            read += 1
            time.sleep(self.pause)
        self.index_path.write_text(json.dumps({"topics": sorted(topics.values(), key=lambda t: t["id"])}, ensure_ascii=False), encoding="utf-8")
        self.progress_path.write_text(json.dumps(prog), encoding="utf-8")
        self._topics = None
        return {"sitemap_pages_read": read, "topics_indexed": len(topics), "pending": len(prog["pending"])}

    def topics(self):
        if self._topics is None:
            self._topics = self._load(self.index_path, {"topics": []}).get("topics", [])
            self._bm25 = BM25([tokens(t["slug"].replace("-", " ")) for t in self._topics])
        return self._topics

    def search(self, query: str, limit: int = 5) -> list[dict]:
        topics = self.topics()
        if not topics:
            return []
        hits = self._bm25.top(tokens(query), k=limit, min_score=1.0)
        return [{"url": f"https://devforum.roblox.com/t/{topics[i]['slug']}/{topics[i]['id']}",
                 "title": topics[i]["slug"].replace("-", " "), "snippet": "", "provider": self.name, "tier": self.tier,
                 "rank_score": round(s, 3), "lastmod": topics[i].get("lastmod")} for i, s in hits]

    def fetch(self, url: str) -> dict:
        m = re.search(r"/t/(?:[^/]+/)?(\d+)", urlparse(url).path)
        if not m:
            raise FetchError("URL DevForum invalide")
        data = json.loads(self.get(f"https://devforum.roblox.com/t/{m.group(1)}.json", accept="application/json"))
        posts = data.get("post_stream", {}).get("posts", [])[:12]
        parts, staff_posts, accepted = [], 0, False
        for post in posts:
            body = strip_html(post.get("cooked", ""))[:5000]
            tag = ""
            if post.get("staff") or post.get("admin") or post.get("moderator"):
                tag, staff_posts = "[PERSONNEL ROBLOX] ", staff_posts + 1
            if post.get("accepted_answer"):
                tag, accepted = tag + "[RÉPONSE ACCEPTÉE] ", True
            parts.append(tag + body)
        return {"title": str(data.get("title", ""))[:200], "text": "\n".join(parts)[:60000],
                "official": staff_posts > 0,
                "meta": {"kind": "forum", "posts_read": len(posts), "staff_posts": staff_posts, "accepted_answer": accepted,
                         "created": str(data.get("created_at", ""))[:10], "last_posted": str(data.get("last_posted_at", ""))[:10]}}


# ---------------------------------------------------------------- GitHub (tier 3)
class GitHub:
    name, tier = "github", 3

    def __init__(self, root: Path = ROOT, getter=http_get):
        self.root, self.get = Path(root), getter

    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Recherche GitHub adaptative, avec requ?tes de secours."""
        words = list(dict.fromkeys(
            w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9_-]*", query)
            if len(w) >= 2
        ))

        if not words:
            return []

        variants = []

        def add(words):
            candidate = " ".join(words[:4])
            if candidate and candidate not in variants:
                variants.append(candidate)

        add(words)

        if len(words) >= 3:
            add([words[0], words[-1]])
            add(words[:2])
        elif len(words) == 2:
            # Ne pas ?largir ? un terme g?n?rique unique.
            # Exemple : "roblox SurfaceAppearance" ne doit
            # jamais devenir simplement "roblox".
            pass

        for q in variants[:3]:
            url = (
                "https://api.github.com/search/repositories?q="
                + quote(q)
                + f"&sort=best-match&per_page={limit}"
            )

            data = json.loads(
                self.get(url, accept="application/vnd.github+json")
            )

            items = data.get("items", [])

            if not items:
                continue

            out = []
            for x in items[:limit]:
                out.append({
                    "url": x.get("html_url", ""),
                    "title": (
                        f"{x.get('full_name', '')} ? "
                        f"{x.get('description') or ''}"
                    ).strip(" ?"),
                    "snippet": " ".join(x.get("topics", [])[:10]),
                    "provider": self.name,
                    "tier": self.tier,
                    "stars": x.get("stargazers_count", 0),
                    "pushed": str(x.get("pushed_at", ""))[:10],
                    "license": (x.get("license") or {}).get("spdx_id")
                })

            return out

        return []

    def fetch(self, url: str) -> dict:
        m = re.match(r"^/([\w.-]{1,100})/([\w.-]{1,100})", urlparse(url).path)
        if urlparse(url).hostname != "github.com" or not m:
            raise FetchError("URL GitHub invalide")
        owner, repo = m.groups()
        meta = json.loads(self.get(f"https://api.github.com/repos/{owner}/{repo}", accept="application/vnd.github+json"))
        try:
            readme = self.get(f"https://api.github.com/repos/{owner}/{repo}/readme", accept="application/vnd.github.raw+json", max_bytes=400_000)
        except FetchError:
            readme = ""
        title = f"{meta.get('full_name', owner + '/' + repo)} — {meta.get('description') or ''}".strip(" —")
        return {"title": title[:200], "text": (str(meta.get("description") or "") + "\n" + readme)[:60000], "official": False,
                "meta": {"kind": "dépôt", "stars": meta.get("stargazers_count"), "pushed": str(meta.get("pushed_at", ""))[:10],
                         "license": (meta.get("license") or {}).get("spdx_id"), "archived": meta.get("archived")}}


# ---------------------------------------------------------------- SearXNG (tier 4, optionnel, sur le PC)
class SearXNG:
    """Moteur de méta-recherche auto-hébergé (gratuit). Activé seulement si VDN_SEARXNG_URL est défini
    (ex. http://localhost:8080). Les pages trouvées ne sont pas téléchargées : seuls les liens vers les hôtes
    autorisés (docs Roblox, DevForum, GitHub) sont transmis aux autres fournisseurs pour lecture."""
    name, tier = "searxng", 4

    def __init__(self, base: str | None = None, getter=http_get):
        self.base = (base or os.getenv("VDN_SEARXNG_URL", "")).rstrip("/")
        self.get = getter

    def available(self) -> bool:
        return bool(self.base)

    def search(self, query: str, limit: int = 8) -> list[dict]:
        if not self.base:
            return []
        host = urlparse(self.base).hostname or ""
        data = json.loads(self.get(f"{self.base}/search?format=json&q=" + quote(query + " roblox"), accept="application/json",
                                   allow_extra_hosts=(host,)) if self.base.startswith("https") else
                          _local_get(f"{self.base}/search?format=json&q=" + quote(query + " roblox")))
        out = []
        for r in data.get("results", [])[: limit * 3]:
            u = r.get("url", "")
            if (urlparse(u).hostname or "") in ("create.roblox.com", "devforum.roblox.com", "github.com"):
                out.append({"url": u, "title": r.get("title", ""), "snippet": r.get("content", "")[:300],
                            "provider": self.name, "tier": self.tier})
            if len(out) >= limit:
                break
        return out


def _local_get(url: str) -> str:
    """Accès HTTP au seul localhost (SearXNG / Ollama sur le PC)."""
    if (urlparse(url).hostname or "") not in ("localhost", "127.0.0.1"):
        raise FetchError("seul localhost est autorisé en http")
    with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=30) as r:
        return r.read(MAX_BYTES).decode("utf-8", "replace")


def provider_for(url: str, providers: dict):
    host = urlparse(url).hostname or ""
    return {"create.roblox.com": providers.get("roblox_docs"), "devforum.roblox.com": providers.get("devforum"),
            "github.com": providers.get("github")}.get(host)
