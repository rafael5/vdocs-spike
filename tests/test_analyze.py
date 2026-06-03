"""Tests for analysis orchestration over Documents (pure)."""

from pathlib import Path

from vdocs_spike.analyze import analyze_all, analyze_doc_type
from vdocs_spike.corpus import Document
from vdocs_spike.parse_pure import Section


def _doc(slug, doc_type, toc, blocks):
    return Document(
        slug=slug,
        path=Path(f"/tmp/{slug}/body.md"),
        doc_type=doc_type,
        app_code="X",
        toc=[Section(a, t, 2) for a, t in toc],
        blocks=blocks,
    )


SHARED = "This boilerplate paragraph recurs across documents in the corpus here."


def test_analyze_doc_type_builds_template_and_boilerplate():
    docs = [
        _doc(
            "a",
            "RN",
            [("intro", "Intro"), ("changes", "Changes")],
            [SHARED, "A-only block of prose text here."],
        ),
        _doc(
            "b",
            "RN",
            [("intro", "Intro")],
            [SHARED, "B-only block of prose text here."],
        ),
        _doc("c", "RN", [("intro", "Intro")], [SHARED]),
    ]
    res = analyze_doc_type("RN", docs, min_docs=2)
    assert res["doc_type"] == "RN"
    assert res["n_docs"] == 3
    assert res["sparse"] is False
    ids = [s["section_id"] for s in res["template"]["sections"]]
    assert "intro" in ids
    # boilerplate recurs in 3 docs and is tagged with the doc_type
    assert len(res["boilerplate"]) == 1
    assert res["boilerplate"][0]["evidence_docs"] == 3
    assert res["boilerplate"][0]["doc_type"] == "RN"


def test_analyze_doc_type_flags_sparse():
    docs = [_doc("solo", "CVG", [("x", "X")], ["only one document of this type."])]
    res = analyze_doc_type("CVG", docs, min_docs=3)
    assert res["sparse"] is True


def test_analyze_all_orders_by_size_desc():
    docs = [
        _doc("a", "RN", [("i", "I")], ["block one of prose text here now."]),
        _doc("b", "RN", [("i", "I")], ["block one of prose text here now."]),
        _doc("c", "TM", [("i", "I")], ["block two of prose text here now."]),
    ]
    out = analyze_all({"TM": [docs[2]], "RN": docs[:2]}, min_docs=2)
    assert [a["doc_type"] for a in out] == ["RN", "TM"]
