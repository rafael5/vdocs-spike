"""Per-doc_type analysis orchestration (pure over :class:`Document` lists).

Combines template induction and boilerplate clustering into one record per
doc_type, which the CLI then serializes to YAML registries and a report.
"""

from __future__ import annotations

from vdocs_spike.boilerplate_pure import cluster_boilerplate
from vdocs_spike.corpus import Document
from vdocs_spike.templates_pure import induce_template


def analyze_doc_type(
    doc_type: str,
    docs: list[Document],
    min_docs: int = 3,
) -> dict:
    """Induce the template and boilerplate for one doc_type's documents."""
    template = induce_template(
        doc_type, [d.toc for d in docs], min_section_docs=min_docs
    )
    blocks_by_doc = {d.slug: d.blocks for d in docs}
    boilerplate = cluster_boilerplate(blocks_by_doc, min_docs=min_docs)
    for rec in boilerplate:
        rec["doc_type"] = doc_type
    return {
        "doc_type": doc_type,
        "n_docs": len(docs),
        "sparse": len(docs) < min_docs,
        "template": template,
        "boilerplate": boilerplate,
    }


def analyze_all(
    grouped: dict[str, list[Document]],
    min_docs: int = 3,
) -> list[dict]:
    """Analyze every doc_type, ordered by descending document count."""
    analyses = [analyze_doc_type(dt, docs, min_docs) for dt, docs in grouped.items()]
    analyses.sort(key=lambda a: (-a["n_docs"], a["doc_type"]))
    return analyses
