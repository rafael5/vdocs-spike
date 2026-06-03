"""Tests for pure template induction (zero I/O)."""

from vdocs_spike.parse_pure import Section
from vdocs_spike.templates_pure import induce_template


def _toc(*pairs):
    """Build a doc's TOC as level-2 sections from (anchor, title) pairs."""
    return [Section(section_id=a, title=t, level=2) for a, t in pairs]


def test_induce_template_scores_evidence_and_required():
    # 3 docs: purpose in all 3, dependencies in 2, oddball in 1.
    docs = [
        _toc(("purpose", "Purpose"), ("dependencies", "Dependencies")),
        _toc(("purpose", "Purpose"), ("dependencies", "Dependencies")),
        _toc(("purpose", "Purpose"), ("oddball", "Oddball")),
    ]
    tpl = induce_template("DIBR", docs, min_section_docs=2)
    assert tpl["doc_type"] == "DIBR"
    assert tpl["evidence_docs"] == 3
    by_id = {s["section_id"]: s for s in tpl["sections"]}
    # oddball appears in only 1 doc -> filtered out by min_section_docs=2
    assert "oddball" not in by_id
    assert by_id["purpose"]["evidence_docs"] == 3
    assert by_id["purpose"]["required"] is True  # 3/3 >= 0.5
    assert by_id["dependencies"]["evidence_docs"] == 2
    assert by_id["dependencies"]["required"] is True  # 2/3 >= 0.5
    assert by_id["purpose"]["toc_level"] is True


def test_induce_template_preserves_order_by_median_position():
    docs = [
        _toc(("a", "A"), ("b", "B"), ("c", "C")),
        _toc(("a", "A"), ("b", "B"), ("c", "C")),
    ]
    tpl = induce_template("RN", docs, min_section_docs=1)
    assert [s["section_id"] for s in tpl["sections"]] == ["a", "b", "c"]


def test_induce_template_optional_below_half():
    docs = [
        _toc(("intro", "Intro")),
        _toc(("intro", "Intro")),
        _toc(("intro", "Intro")),
        _toc(("appendix", "Appendix")),  # 1/4 = 0.25 -> optional
    ]
    tpl = induce_template("TM", docs, min_section_docs=1)
    by_id = {s["section_id"]: s for s in tpl["sections"]}
    assert by_id["intro"]["required"] is True
    assert by_id["appendix"]["required"] is False


def test_induce_template_id_is_stable_and_doctype_prefixed():
    docs = [_toc(("a", "A"), ("b", "B"))]
    t1 = induce_template("DG", docs, min_section_docs=1)
    t2 = induce_template("DG", docs, min_section_docs=1)
    assert t1["template_id"] == t2["template_id"]
    assert t1["template_id"].startswith("DG:")


def test_induce_template_distinguishes_levels():
    docs = [
        [Section("setup", "Setup", 2), Section("setup", "Setup", 3)],
        [Section("setup", "Setup", 2), Section("setup", "Setup", 3)],
    ]
    tpl = induce_template("IG", docs, min_section_docs=1)
    levels = sorted(s["level"] for s in tpl["sections"])
    assert levels == [2, 3]


def test_induce_template_ratio_floor_drops_long_tail():
    # 20 docs: 'core' in all 20, 'noise' in 2. With a 0.2 ratio floor the
    # effective floor is max(min_section_docs=1, round(0.2*20)=4) = 4, so the
    # 2-doc 'noise' section is dropped while 'core' survives.
    docs = [_toc(("core", "Core"))] * 18 + [
        _toc(("core", "Core"), ("noise", "Noise")),
        _toc(("core", "Core"), ("noise", "Noise")),
    ]
    tpl = induce_template("DIBR", docs, min_section_docs=1, template_ratio=0.2)
    ids = {s["section_id"] for s in tpl["sections"]}
    assert "core" in ids
    assert "noise" not in ids


def test_induce_template_empty_docs_returns_empty_sections():
    tpl = induce_template("CVG", [], min_section_docs=1)
    assert tpl["sections"] == []
    assert tpl["evidence_docs"] == 0
