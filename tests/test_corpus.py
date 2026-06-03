"""Tests for the thin corpus I/O driver (real files in a tmp dir)."""

from pathlib import Path

from vdocs_spike.corpus import discover, group_by_doc_type, load_document

DOC_A = """---
doc_type: RN
app_code: PSO
version: '1.0'
---

# Pharmacy Release Notes

## Contents

- [Overview](#overview)
- [Changes](#changes)

## Overview

Shared intro paragraph that two docs have in common here.

## Changes

Doc A specific change list goes in this paragraph only.
"""

DOC_B = """---
doc_type: RN
app_code: PSO
version: '2.0'
---

# Pharmacy Release Notes 2

## Contents

- [Overview](#overview)

## Overview

Shared intro paragraph that two docs have in common here.
"""


def _write(root: Path, pkg: str, slug: str, text: str) -> None:
    d = root / pkg / slug
    d.mkdir(parents=True)
    (d / "body.md").write_text(text)


def test_discover_finds_body_md(tmp_path):
    _write(tmp_path, "PSO", "doc_a", DOC_A)
    _write(tmp_path, "PSO", "doc_b", DOC_B)
    found = discover(tmp_path)
    assert len(found) == 2
    assert all(p.name == "body.md" for p in found)


def test_load_document_parses_frontmatter_toc_blocks(tmp_path):
    _write(tmp_path, "PSO", "doc_a", DOC_A)
    doc = load_document(tmp_path / "PSO" / "doc_a" / "body.md")
    assert doc.doc_type == "RN"
    assert doc.app_code == "PSO"
    assert doc.slug == "doc_a"
    assert [s.section_id for s in doc.toc] == ["overview", "changes"]
    assert any("Shared intro paragraph" in b for b in doc.blocks)


def test_group_by_doc_type(tmp_path):
    _write(tmp_path, "PSO", "doc_a", DOC_A)
    _write(tmp_path, "PSO", "doc_b", DOC_B)
    docs = [load_document(p) for p in discover(tmp_path)]
    grouped = group_by_doc_type(docs)
    assert set(grouped) == {"RN"}
    assert len(grouped["RN"]) == 2


def test_load_document_missing_doc_type_defaults_unknown(tmp_path):
    _write(tmp_path, "X", "nofm", "# No frontmatter\n\nbody text here.\n")
    doc = load_document(tmp_path / "X" / "nofm" / "body.md")
    assert doc.doc_type == "UNKNOWN"
