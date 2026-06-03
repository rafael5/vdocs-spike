"""Pure template induction over a doc_type's TOC sequences (zero I/O).

Given every document's parsed ``## Contents`` (as ``Section`` lists), induce the
recurring section skeleton: union the sections, score each by how many docs
contain it, order by median TOC position, and mark required vs optional. The
emitted record is schema-compatible with ``vdocs`` ``registries/templates``.
"""

from __future__ import annotations

import hashlib
from statistics import median

from vdocs_spike.parse_pure import Section


def _template_id(doc_type: str, ordered_section_ids: list[str]) -> str:
    digest = hashlib.sha256("\n".join(ordered_section_ids).encode()).hexdigest()
    return f"{doc_type}:{digest[:8]}"


def induce_template(
    doc_type: str,
    toc_lists: list[list[Section]],
    min_section_docs: int = 2,
    required_ratio: float = 0.5,
    template_ratio: float = 0.2,
) -> dict:
    """Induce the section template for one ``doc_type``.

    ``toc_lists`` is one parsed TOC (list of sections) per document. A section is
    keyed by ``(section_id, level)``; ``evidence_docs`` counts distinct docs that
    contain it. A section joins the template only when it clears the evidence
    floor ``max(min_section_docs, round(template_ratio * total))`` — the ratio
    term scales the floor with corpus size so a 120-doc type's one-off sections
    are dropped without over-pruning a 4-doc type. ``required`` is true when
    coverage reaches ``required_ratio``.
    """
    total = len(toc_lists)
    floor = max(min_section_docs, round(template_ratio * total))
    # Aggregate per (section_id, level): doc count, positions, first-seen title.
    agg: dict[tuple[str, int], dict] = {}
    for toc in toc_lists:
        seen: set[tuple[str, int]] = set()
        for pos, sec in enumerate(toc):
            key = (sec.section_id, sec.level)
            rec = agg.setdefault(key, {"title": sec.title, "docs": 0, "positions": []})
            rec["positions"].append(pos)
            if key not in seen:
                rec["docs"] += 1
                seen.add(key)

    sections = []
    for (section_id, level), rec in agg.items():
        if rec["docs"] < floor:
            continue
        sections.append(
            {
                "section_id": section_id,
                "title": rec["title"],
                "level": level,
                "required": total > 0 and rec["docs"] / total >= required_ratio,
                "toc_level": True,
                "evidence_docs": rec["docs"],
                "_median_pos": median(rec["positions"]),
            }
        )

    # Order by median TOC position, tie-break on stronger evidence then id.
    sections.sort(
        key=lambda s: (s["_median_pos"], -s["evidence_docs"], s["section_id"])
    )
    for s in sections:
        del s["_median_pos"]

    return {
        "template_id": _template_id(doc_type, [s["section_id"] for s in sections]),
        "doc_type": doc_type,
        "evidence_docs": total,
        "sections": sections,
    }
