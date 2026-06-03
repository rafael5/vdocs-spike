"""Thin I/O driver: discover and load the normalized corpus into Documents.

All parsing is delegated to the pure transforms in :mod:`vdocs_spike.parse_pure`;
this module only touches the filesystem.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from vdocs_spike.parse_pure import (
    Section,
    parse_toc,
    split_blocks,
    split_frontmatter,
)

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class Document:
    """One normalized document: metadata plus its parsed TOC and prose blocks."""

    slug: str
    path: Path
    doc_type: str
    app_code: str
    frontmatter: dict = field(default_factory=dict)
    toc: list[Section] = field(default_factory=list)
    blocks: list[str] = field(default_factory=list)


def discover(root: Path) -> list[Path]:
    """Find every ``body.md`` under ``root`` (sorted for deterministic runs)."""
    return sorted(root.rglob("body.md"))


def load_document(path: Path) -> Document:
    """Read and parse a single ``body.md`` into a :class:`Document`."""
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    return Document(
        slug=path.parent.name,
        path=path,
        doc_type=str(frontmatter.get("doc_type", "UNKNOWN")),
        app_code=str(frontmatter.get("app_code", "")),
        frontmatter=frontmatter,
        toc=parse_toc(body),
        blocks=split_blocks(body),
    )


def load_corpus(root: Path) -> list[Document]:
    """Discover and load every document under ``root``."""
    docs = [load_document(p) for p in discover(root)]
    log.info("loaded %d documents from %s", len(docs), root)
    return docs


def group_by_doc_type(docs: list[Document]) -> dict[str, list[Document]]:
    """Partition documents by ``doc_type`` (ordered by descending group size)."""
    grouped: dict[str, list[Document]] = defaultdict(list)
    for doc in docs:
        grouped[doc.doc_type].append(doc)
    return dict(sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])))
