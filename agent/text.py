"""Outils texte partagés (bibliothèque standard uniquement) : découpage en mots, vocabulaire, BM25.

Aucune dépendance externe : fonctionne dans GitHub Actions comme sur Windows.
"""
from __future__ import annotations
import json
import math
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Mots vides (français + anglais) : ils ne doivent jamais compter dans la pertinence.
STOP = set("""
a an and are as at be by for from has have how in into is it its of on or that the this to was what when where which
with without why you your can could should would do does did not no yes using use used via vs about over under than
then there these those will just like get got make made best good new all any some very more most also only out up
le la les un une des du de d l et en est sont pour par dans sur avec sans que qui quoi comment pourquoi au aux ce cet
cette ces se sa son ses leur leurs ou où mais donc car ne pas plus moins très tout tous toute toutes
implementation limitations troubleshooting realistic help question issue problem anyone please thanks thank
""".split())

_WORD = re.compile(r"[a-z0-9][a-z0-9_]*")


def fold(text: str) -> str:
    """Minuscules sans accents (é -> e), pour comparer français et anglais."""
    text = unicodedata.normalize("NFKD", str(text or "")).encode("ascii", "ignore").decode("ascii")
    return text.lower()


def stem(word: str) -> str:
    """Racinisation légère et prévisible (pluriels simples), suffisante pour un vocabulaire technique."""
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("es") and word[-3] in "sxz":
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokens(text: str, keep_stop: bool = False) -> list[str]:
    out = []
    for w in _WORD.findall(fold(text).replace("-", " ").replace("/", " ")):
        if not keep_stop and (w in STOP or len(w) < 2):
            continue
        out.append(stem(w))
    return out


@lru_cache(maxsize=4)
def vocabulary(path: str | None = None) -> dict:
    p = Path(path) if path else ROOT / "config" / "vocabulary.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["_syn_index"] = {}
    for concept, words in data.get("synonyms", {}).items():
        for w in words:
            data["_syn_index"].setdefault(stem(fold(w)), set()).add(concept)
    return data


def concepts(text_tokens) -> set[str]:
    """Concepts du vocabulaire présents (ex. « needles » -> foliage)."""
    idx = vocabulary()["_syn_index"]
    found = set()
    for t in text_tokens:
        found |= idx.get(t, set())
    return found


def expand(term: str) -> list[str]:
    """Synonymes d'un terme (lui compris), pour élargir une requête sans la rallonger."""
    voc = vocabulary()
    t = stem(fold(term))
    for concept, words in voc.get("synonyms", {}).items():
        stems = [stem(fold(w)) for w in words]
        if t in stems or t == stem(concept):
            return list(dict.fromkeys([term] + words))
    return [term]


def contains_phrase(text: str, phrase: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(fold(phrase)) + r"(?![a-z0-9])", fold(text)) is not None


class BM25:
    """BM25 classique (k1=1.5, b=0.75) sur une petite collection en mémoire."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.docs = docs
        self.k1, self.b = k1, b
        self.n = len(docs)
        self.avgdl = (sum(len(d) for d in docs) / self.n) if self.n else 0.0
        self.df: dict[str, int] = {}
        self.tf: list[dict[str, int]] = []
        for d in docs:
            freq: dict[str, int] = {}
            for w in d:
                freq[w] = freq.get(w, 0) + 1
            self.tf.append(freq)
            for w in freq:
                self.df[w] = self.df.get(w, 0) + 1

    def idf(self, w: str) -> float:
        df = self.df.get(w, 0)
        return math.log(1 + (self.n - df + 0.5) / (df + 0.5))

    def score(self, query: list[str], i: int) -> float:
        freq, dl = self.tf[i], len(self.docs[i]) or 1
        s = 0.0
        for w in set(query):
            f = freq.get(w, 0)
            if f:
                s += self.idf(w) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / (self.avgdl or 1)))
        return s

    def top(self, query: list[str], k: int = 10, min_score: float = 0.0) -> list[tuple[int, float]]:
        scored = [(i, self.score(query, i)) for i in range(self.n)]
        scored = [x for x in scored if x[1] > min_score]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


def approx_tokens(text: str) -> int:
    """Estimation prudente du nombre de tokens d'un texte (≈ 4 caractères par token, arrondi au-dessus)."""
    return max(1, math.ceil(len(text) / 3.6))
