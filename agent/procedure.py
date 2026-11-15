"""Conservative evidence check: excerpts are not automatically instructions.

A procedure needs an explicit operation plus an identifiable technical object,
not merely a table of contents or a list of possible topics.
"""
from __future__ import annotations
import re

ACTION = re.compile(r"(?i)\b(?:set|enable|disable|change|adjust|configure|select|click|open|export|import|bake|assign|connect|apply|create|add|remove|paint|unwrap|duplicate|parent|weight|r[eé]gle[rz]?|active[rz]?|d[eé]sactive[rz]?|s[eé]lectionne[rz]?|exporte[rz]?|importe[rz]?|applique[rz]?|ajoute[rz]?|cr[eé]e[rz]?)\b")
OBJECT = re.compile(r"(?i)\b(?:alphamode|colormap|normalmap|roughnessmap|surfaceappearance|meshpart|materialvariant|blender|uv|texture|mesh|material|modifier|shader|vertex|vertices|bone|armature|transparency|opacity|normal map|atlas|fbx|spotlight|lighting|terrain|particle|node|property|propert(?:y|ies)|param[eè]tre|mat[eé]riau|maillage|transparence|branche|branch|foliage|leaf|leaves)\b")
TOC = re.compile(r"(?i)^\s*(?:[-*#]+\s*)?(?:\d+[.)]\s*)?(?:introduction|overview|contents|table of contents|tutorial|step \d+|chapter \d+|conclusion|optimization|optimisation|uv mapping|texture atlases|pbr|materials?|feuillage|transparency|transparence)\s*[:.]?\s*$")

def actionable_excerpts(excerpts: list[str]) -> list[str]:
    """Only clear action+object evidence; not proof of correctness or Roblox testing."""
    return [s for s in excerpts if not TOC.match(s) and ACTION.search(s) and OBJECT.search(s)]
