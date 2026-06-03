"""Pure parsing transforms for the normalized VistA corpus (zero I/O).

Every function here takes/returns plain values and performs no side effects, so
each is independently testable with inline fixtures and Hypothesis properties.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import yaml

_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
_TOC_LINK_RE = re.compile(r"^\s*[-*]\s*\[(?P<title>.+?)\]\(#(?P<anchor>[^)]*)\)\s*$")
_HEADING_RE = re.compile(r"^#{1,6}\s")
_WS_RE = re.compile(r"\s+")
# A line that is *entirely* a markdown link/image/table-marker artifact — nav
# links, secondary plain-text TOC entries, figure images, CSV table pointers —
# i.e. structure, not prose. Inline links inside real sentences are not matched
# (the pattern is anchored and the bracket text cannot contain prose tails).
_ARTIFACT_RE = re.compile(
    r"^\s*(?:"
    r"<img\b[^>]*>"  # figure image
    r"|[_*↑\s]*\[.*\]\([^)]*\)[_*\s]*"  # link/TOC/table-marker only line
    r")\s*$"
)


@dataclass(frozen=True)
class Section:
    """One TOC entry: its anchor slug, display title, and heading level."""

    section_id: str
    title: str
    level: int


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Split leading ``---`` YAML frontmatter from the markdown body.

    Returns ``({}, text)`` unchanged when there is no frontmatter block.
    """
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    data = yaml.safe_load(match.group(1)) or {}
    if not isinstance(data, dict):
        return {}, text
    return data, text[match.end() :]


def parse_toc(body: str) -> list[Section]:
    """Parse the ``## Contents`` markdown list into ordered :class:`Section`s.

    Indentation drives nesting: top-level items are level 2, every two leading
    spaces adds one level (matching the registry's ``level``/``toc_level``).
    """
    lines = body.splitlines()
    sections: list[Section] = []
    in_toc = False
    for line in lines:
        stripped = line.strip()
        if not in_toc:
            if stripped.lower() == "## contents":
                in_toc = True
            continue
        # End the TOC at the next real heading.
        if _HEADING_RE.match(line):
            break
        match = _TOC_LINK_RE.match(line)
        if not match:
            continue
        indent = len(line) - len(line.lstrip(" "))
        level = 2 + indent // 2
        sections.append(
            Section(
                section_id=match.group("anchor"),
                title=match.group("title").strip(),
                level=level,
            )
        )
    return sections


def split_blocks(body: str) -> list[str]:
    """Split a body into prose blocks (paragraphs) for boilerplate detection.

    Blocks are separated by blank lines. Heading lines and table-of-contents
    link lines are dropped so only candidate prose remains.
    """
    blocks: list[str] = []
    for chunk in re.split(r"\n\s*\n", body):
        kept = [
            ln
            for ln in chunk.splitlines()
            if (
                ln.strip()
                and not _HEADING_RE.match(ln)
                and not _TOC_LINK_RE.match(ln)
                and not _ARTIFACT_RE.match(ln)
            )
        ]
        if not kept:
            continue
        text = "\n".join(kept).strip()
        if text:
            blocks.append(text)
    return blocks


def block_key(text: str) -> str:
    """Whitespace-collapsed, lowercased match identity for a block.

    Idempotent: ``block_key(block_key(x)) == block_key(x)``.
    """
    return _WS_RE.sub(" ", text).strip().lower()


def shingles(text: str, n: int = 3) -> frozenset[str]:
    """Word n-gram shingle set over the block key, for near-dup Jaccard.

    Falls back to a single whole-text shingle when there are fewer than ``n``
    words.
    """
    words = block_key(text).split()
    if len(words) < n:
        return frozenset({" ".join(words)}) if words else frozenset()
    return frozenset(" ".join(words[i : i + n]) for i in range(len(words) - n + 1))
