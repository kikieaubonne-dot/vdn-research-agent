"""Structured analysis of candidate technical instructions."""

from __future__ import annotations

from dataclasses import dataclass, asdict

from agent.procedure import ACTION, OBJECT, actionable_excerpts


@dataclass
class ProcedureEvidence:
    text: str
    action: str | None
    object: str | None
    status: str
    tested: bool = False


def analyze_procedures(excerpts: list[str]) -> list[dict]:
    """Analyze actionable evidence without claiming tutorial completeness."""

    accepted = actionable_excerpts(excerpts)
    results = []

    for excerpt in accepted:
        action = ACTION.search(excerpt)
        obj = OBJECT.search(excerpt)

        evidence = ProcedureEvidence(
            text=excerpt,
            action=action.group(0) if action else None,
            object=obj.group(0) if obj else None,
            status="candidate_instruction",
            tested=False,
        )

        results.append(asdict(evidence))

    return results
