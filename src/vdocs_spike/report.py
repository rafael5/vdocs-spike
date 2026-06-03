"""Pure rendering of analyses into registry-YAML objects and a markdown report.

The YAML objects are schema-compatible with ``vdocs`` ``registries/templates`` and
``registries/boilerplate`` so findings can be hand-merged. The markdown report is
the human-readable deliverable.
"""

from __future__ import annotations


def templates_yaml_obj(analyses: list[dict]) -> dict:
    """Build the ``{"templates": [...]}`` registry object.

    Sparse doc_types and templates with no induced sections are excluded — there
    is nothing curation-worthy to emit for them.
    """
    templates = [
        a["template"] for a in analyses if not a["sparse"] and a["template"]["sections"]
    ]
    return {"templates": templates}


def boilerplate_yaml_obj(analyses: list[dict], top_n: int = 50) -> dict:
    """Build the ``{"boilerplate": [...]}`` registry object across all doc_types.

    Each doc_type's blocks are already sorted by descending evidence; only the
    top ``top_n`` per type are emitted so the registry stays curation-sized
    rather than dumping the long tail of short low-value fragments.
    """
    records = [rec for a in analyses for rec in a["boilerplate"][:top_n]]
    return {"boilerplate": records}


def _required_count(analysis: dict) -> int:
    return sum(1 for s in analysis["template"]["sections"] if s["required"])


def _status(analysis: dict) -> str:
    """Tier a doc_type by the strength of its induced required skeleton."""
    if analysis["sparse"]:
        return "sparse"
    n_req = _required_count(analysis)
    if n_req >= 5:
        return "strong"
    if n_req >= 1:
        return "weak"
    return "noisy"


def render_report(analyses: list[dict], min_docs: int, max_rows: int = 45) -> str:
    """Render the per-doc_type human-readable markdown report."""
    total_docs = sum(a["n_docs"] for a in analyses)
    lines: list[str] = []
    lines.append("# VistA corpus template & boilerplate induction")
    lines.append("")
    lines.append(
        f"Analyzed **{total_docs}** documents across **{len(analyses)}** doc_types "
        f"(min-docs threshold = {min_docs})."
    )
    lines.append("")
    lines.append(
        "`status`: **strong** = ≥5 required sections (clean template); "
        "**weak** = 1–4 required; **noisy** = sections found but none recurring "
        "enough to be required; **sparse** = too few docs to induce."
    )
    lines.append("")

    # Summary table.
    lines.append("| doc_type | docs | sections | required | boilerplate | status |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for a in analyses:
        n_sections = len(a["template"]["sections"])
        lines.append(
            f"| {a['doc_type']} | {a['n_docs']} | {n_sections} | "
            f"{_required_count(a)} | {len(a['boilerplate'])} | {_status(a)} |"
        )
    lines.append("")

    # Notes for curators — computed caveats so the status column isn't misread.
    small_strong = [
        a["doc_type"] for a in analyses if _status(a) == "strong" and a["n_docs"] < 10
    ]
    heterogeneous = [
        a["doc_type"]
        for a in analyses
        if _status(a) == "noisy" and a["template"]["sections"]
    ]
    lines.append("## Notes for curators")
    lines.append("")
    strong_big = [
        a["doc_type"] for a in analyses if _status(a) == "strong" and a["n_docs"] >= 10
    ]
    lines.append(
        "- **Promote with confidence:** "
        + (", ".join(f"`{dt}`" for dt in strong_big) or "_none_")
        + " — corpus-wide standardized template (many docs, high coverage)."
    )
    lines.append(
        "- **Small-cohort 'strong' (verify before promoting):** "
        + (", ".join(f"`{dt}`" for dt in small_strong) or "_none_")
        + " — < 10 docs, so a near-duplicate handful can manufacture a 'template'"
        " that won't generalize."
    )
    lines.append(
        "- **Heterogeneous (sections found, none required):** "
        + (", ".join(f"`{dt}`" for dt in heterogeneous) or "_none_")
        + " — exact-anchor alignment is defeated by numbered/renamed headings;"
        " would need fuzzy heading alignment to induce a skeleton."
    )
    lines.append(
        "- Boilerplate blocks are exact/near-duplicate prose recurring across"
        " ≥ min-docs of a type, sorted by evidence; the top entries per type are"
        " the curation-worthy ones (the long tail is short fragments)."
    )
    lines.append("")

    # Per-doc_type detail.
    for a in analyses:
        dt = a["doc_type"]
        lines.append(f"## {dt} — {a['n_docs']} docs ({_status(a)})")
        lines.append("")
        if a["sparse"]:
            lines.append(
                f"_Too sparse ({a['n_docs']} < {min_docs}) to induce a reliable "
                "template or boilerplate set._"
            )
            lines.append("")
            continue

        sections = a["template"]["sections"]
        lines.append(
            f"**Template** `{a['template']['template_id']}` — {len(sections)} "
            f"sections, {_required_count(a)} required"
        )
        lines.append("")
        if sections:
            lines.append("| level | section | required | evidence |")
            lines.append("|---:|---|:--:|---:|")
            for s in sections[:max_rows]:
                req = "✓" if s["required"] else "·"
                indent = "&nbsp;" * (2 * (s["level"] - 2))
                lines.append(
                    f"| {s['level']} | {indent}{s['title']} | {req} | "
                    f"{s['evidence_docs']}/{a['n_docs']} |"
                )
            if len(sections) > max_rows:
                lines.append(
                    f"| | _… and {len(sections) - max_rows} more (low-evidence "
                    "tail)_ | | |"
                )
        else:
            lines.append("_No consistent section structure induced (noisy)._")
        lines.append("")

        bp = a["boilerplate"]
        lines.append(f"**Boilerplate** — {len(bp)} recurring blocks")
        lines.append("")
        if bp:
            for rec in bp[:15]:
                snippet = rec["text"].splitlines()[0].strip()
                if len(snippet) > 90:
                    snippet = snippet[:90].rstrip() + "…"
                lines.append(f"- `{rec['evidence_docs']}×` {snippet}")
            if len(bp) > 15:
                lines.append(f"- _… and {len(bp) - 15} more_")
        else:
            lines.append("_No recurring verbatim blocks above threshold._")
        lines.append("")

    return "\n".join(lines) + "\n"
