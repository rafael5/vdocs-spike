"""Tests for pure boilerplate clustering (zero I/O)."""

from vdocs_spike.boilerplate_pure import cluster_boilerplate


def test_cluster_keeps_blocks_recurring_across_min_docs():
    shared = "When prompted 'Want KIDS to INHIBIT LOGONs? NO//', answer NO."
    blocks_by_doc = {
        "d1": [shared, "Unique to d1 entirely different sentence here."],
        "d2": [shared, "Unique to d2 entirely different sentence here."],
        "d3": [shared],
    }
    out = cluster_boilerplate(blocks_by_doc, min_docs=3, min_chars=10)
    assert len(out) == 1
    rec = out[0]
    assert rec["evidence_docs"] == 3
    assert rec["text"] == shared
    assert rec["key"] == shared.lower().replace("  ", " ")
    assert rec["id"].startswith("bp-")
    assert rec["label"]  # non-empty human label


def test_cluster_drops_blocks_below_min_docs():
    blocks_by_doc = {
        "d1": ["Only appears once in the whole corpus here."],
        "d2": ["A different singleton block of prose text."],
    }
    out = cluster_boilerplate(blocks_by_doc, min_docs=2, min_chars=10)
    assert out == []


def test_cluster_counts_distinct_docs_not_occurrences():
    shared = "This repeated paragraph occurs many times in one doc only here."
    blocks_by_doc = {"d1": [shared, shared, shared]}
    out = cluster_boilerplate(blocks_by_doc, min_docs=2, min_chars=10)
    assert out == []  # only 1 distinct doc


def test_cluster_ignores_short_blocks():
    blocks_by_doc = {"d1": ["ok"], "d2": ["ok"], "d3": ["ok"]}
    out = cluster_boilerplate(blocks_by_doc, min_docs=2, min_chars=10)
    assert out == []


def test_cluster_merges_near_duplicates():
    # Same block save for a trailing word -> should cluster together via shingles.
    a = "The purpose of this plan is to provide a common deployment document."
    b = "The purpose of this plan is to provide a common deployment document now."
    blocks_by_doc = {"d1": [a], "d2": [b], "d3": [a]}
    out = cluster_boilerplate(blocks_by_doc, min_docs=3, min_chars=10, jaccard=0.6)
    assert len(out) == 1
    assert out[0]["evidence_docs"] == 3


def test_cluster_sorted_by_evidence_desc():
    common = "Common block shared across all three documents in the set here."
    pair = "Pair block shared across two of the documents only in set."
    blocks_by_doc = {
        "d1": [common, pair],
        "d2": [common, pair],
        "d3": [common],
    }
    out = cluster_boilerplate(blocks_by_doc, min_docs=2, min_chars=10)
    assert [r["evidence_docs"] for r in out] == [3, 2]


def test_cluster_id_stable_for_same_key():
    shared = "A stable boilerplate paragraph that recurs across documents in corpus."
    b1 = {"d1": [shared], "d2": [shared]}
    b2 = {"x9": [shared], "x8": [shared]}
    out1 = cluster_boilerplate(b1, min_docs=2, min_chars=10)
    out2 = cluster_boilerplate(b2, min_docs=2, min_chars=10)
    assert out1[0]["id"] == out2[0]["id"]
