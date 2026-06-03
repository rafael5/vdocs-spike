"""Tests for pure parsing transforms (zero I/O)."""

from hypothesis import given
from hypothesis import strategies as st

from vdocs_spike.parse_pure import (
    Section,
    block_key,
    parse_toc,
    shingles,
    split_blocks,
    split_frontmatter,
)

# --- split_frontmatter -------------------------------------------------------

SAMPLE = """---
title: Foo Bar Guide
doc_type: DIBR
version: '4.5'
---

# Foo Bar Guide

## Contents

- [Purpose](#purpose)

## Purpose

Hello world.
"""


def test_split_frontmatter_parses_yaml_and_returns_body():
    fm, body = split_frontmatter(SAMPLE)
    assert fm["doc_type"] == "DIBR"
    assert fm["version"] == "4.5"
    assert body.lstrip().startswith("# Foo Bar Guide")
    assert "doc_type" not in body


def test_split_frontmatter_no_frontmatter_returns_empty_dict():
    text = "# No frontmatter here\n\nbody"
    fm, body = split_frontmatter(text)
    assert fm == {}
    assert body == text


def test_split_frontmatter_handles_empty_string():
    fm, body = split_frontmatter("")
    assert fm == {}
    assert body == ""


# --- parse_toc ---------------------------------------------------------------

TOC_BODY = """# Title

## Contents

- [Purpose](#purpose)
- [Site Readiness](#site-readiness)
  - [Site Preparation](#site-preparation)
    - [Hardware](#hardware)
- [Resources](#resources)

## Purpose

Body text not in toc.
"""


def test_parse_toc_extracts_ordered_sections_with_levels():
    secs = parse_toc(TOC_BODY)
    assert [s.section_id for s in secs] == [
        "purpose",
        "site-readiness",
        "site-preparation",
        "hardware",
        "resources",
    ]
    assert secs[0] == Section(section_id="purpose", title="Purpose", level=2)
    # two-space indent -> level 3, four-space -> level 4
    assert secs[2].level == 3
    assert secs[3].level == 4
    assert secs[4].level == 2


def test_parse_toc_returns_empty_when_no_contents_heading():
    assert parse_toc("# Title\n\nNo contents here.\n") == []


# --- split_blocks ------------------------------------------------------------


def test_split_blocks_drops_headings_and_toc_links():
    blocks = split_blocks(TOC_BODY)
    # The only prose block is the body text; headings and toc links are dropped.
    assert blocks == ["Body text not in toc."]


def test_split_blocks_drops_markdown_artifacts():
    body = (
        "## Body\n\n"
        "Real prose paragraph worth keeping here.\n\n"
        "[↑ Back to Contents](#contents)\n\n"
        "[1 Introduction [1](#introduction)](#introduction)\n\n"
        '<img src="abc.jpeg" title="Figure">\n\n'
        "_[Table 1 (extracted to CSV)](tables/table-01.csv)_\n"
    )
    blocks = split_blocks(body)
    assert blocks == ["Real prose paragraph worth keeping here."]


def test_split_blocks_keeps_prose_with_inline_link():
    body = "See the [docs](http://x) for more details and context here.\n"
    assert split_blocks(body) == [
        "See the [docs](http://x) for more details and context here."
    ]


def test_split_blocks_splits_on_blank_lines():
    body = "First paragraph here.\n\nSecond paragraph here.\n"
    assert split_blocks(body) == [
        "First paragraph here.",
        "Second paragraph here.",
    ]


# --- block_key ---------------------------------------------------------------


def test_block_key_collapses_whitespace_and_lowercases():
    assert block_key("  Hello   WORLD\n\tFoo  ") == "hello world foo"


def test_block_key_idempotent_example():
    once = block_key("The  QUICK\n brown Fox")
    assert block_key(once) == once


@given(st.text())
def test_block_key_is_idempotent(text):
    once = block_key(text)
    assert block_key(once) == once


@given(st.text())
def test_block_key_has_no_double_spaces_or_edge_space(text):
    key = block_key(text)
    assert "  " not in key
    assert key == key.strip()
    assert key == key.lower()


# --- shingles ----------------------------------------------------------------


def test_shingles_word_ngrams():
    sh = shingles("the quick brown fox", n=2)
    assert ("the quick") in sh
    assert ("quick brown") in sh
    assert ("brown fox") in sh
    assert len(sh) == 3


def test_shingles_short_text_returns_whole():
    sh = shingles("oneword", n=3)
    assert sh == frozenset({"oneword"})
