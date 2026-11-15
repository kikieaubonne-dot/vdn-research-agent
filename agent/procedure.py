"""Conservative detection of complete, actionable technical evidence.

A single instruction is not a complete tutorial. Evidence is not Studio validation.
"""
from __future__ import annotations
import re

ACTION = re.compile(r"(?i)\b(?:set|enable|disable|change|adjust|configure|select|click|open|export|import|bake|assign|connect|apply|create|add|remove|paint|unwrap|duplicate|parent|weight|use|reuse|test|check|measure|inspect|choose|try\s+to\s+use|r[eé]gle[rz]?|active[rz]?|d[eé]sactive[rz]?|s[eé]lectionne[rz]?|exporte[rz]?|importe[rz]?|applique[rz]?|ajoute[rz]?|cr[eé]e[rz]?)\b")
OBJECT = re.compile(r"(?i)\b(?:alphamode|colormap|normalmap|roughnessmap|surfaceappearance|meshpart|materialvariant|blender|uv|textures?|meshes?|materials?|modifier|shader|vertex|vertices|bones?|armature|transparency|opacity|normal map|atlas|fbx|spotlight|lighting|terrain|particles?|nodes?|propert(?:y|ies)|param[eè]tre|mat[eé]riau|maillage|transparence|branches?|foliage|leaf|leaves|draw calls?|triangles?|streaming|frame rate)\b")
TOC = re.compile(r"(?i)^\s*(?:[-*#]+\s*)?(?:\d+[.)]\s*)?(?:introduction|overview|contents|table of contents|tutorial|step \d+|chapter \d+|conclusion|optimization|optimisation|uv mapping|texture atlases|pbr|materials?|feuillage|transparency|transparence)\s*[:.]?\s*$")
TRAILING = re.compile(r"(?i)\b(?:to|of|with|in|on|at|for|from|into|as|by|and|or|the|a|an|de|du|des|dans|sur|avec|pour|à|au|aux|une?|les?)\s*$")
MARKDOWN_LINK = re.compile(r"\[([^]]+)\]\([^)]+\)")


def actionable_excerpts(excerpts: list[str]) -> list[str]:
    """Return only self-contained action+object excerpts; not a tutorial verdict."""
    result = []
    for raw in excerpts:
        s = MARKDOWN_LINK.sub(r"\1", str(raw)).strip()
        s = re.sub(r"\s+", " ", s)
        if (len(s) < 35 or TOC.fullmatch(s) or s.endswith(('...', '…', ':', ',', ';', '-', '—'))
                or TRAILING.search(s) or not ACTION.search(s) or not OBJECT.search(s)):
            continue
        # A bare section heading or property name is never a complete instruction.
        if s.startswith('#') or re.fullmatch(r"(?i)(?:property|class):\s*[\w.]+", s):
            continue
        result.append(raw)
    return result
