"""Pure boilerplate clustering within a doc_type (zero I/O).

Group body blocks by their :func:`~vdocs_spike.parse_pure.block_key` (exact,
whitespace-collapsed match identity), then merge near-duplicate clusters by
shingle Jaccard. Clusters recurring across at least ``min_docs`` distinct
documents become records schema-compatible with ``vdocs`` ``registries/boilerplate``.
"""

from __future__ import annotations

import hashlib
from collections import Counter

from vdocs_spike.parse_pure import block_key, shingles


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / len(a | b)


def _bp_id(key: str) -> str:
    return "bp-" + hashlib.sha256(key.encode()).hexdigest()[:10]


def _label(text: str, width: int = 50) -> str:
    """First line of canonical text, trimmed to a short human label."""
    first = text.strip().splitlines()[0].strip()
    return first if len(first) <= width else first[:width].rstrip()


def cluster_boilerplate(
    blocks_by_doc: dict[str, list[str]],
    min_docs: int = 3,
    min_chars: int = 20,
    jaccard: float = 0.8,
    shingle_n: int = 4,
) -> list[dict]:
    """Cluster recurring verbatim/near-verbatim blocks across docs of one type.

    ``blocks_by_doc`` maps a doc id to its prose blocks. Returns one record per
    cluster present in ``>= min_docs`` distinct docs, sorted by ``evidence_docs``
    descending. Blocks shorter than ``min_chars`` are ignored as noise.
    """
    # 1. Exact block_key grouping. Track distinct docs + original-text votes.
    groups: dict[str, dict] = {}
    for doc_id, blocks in blocks_by_doc.items():
        for raw in blocks:
            if len(raw.strip()) < min_chars:
                continue
            key = block_key(raw)
            if len(key) < min_chars:
                continue
            grp = groups.setdefault(
                key,
                {
                    "docs": set(),
                    "texts": Counter(),
                    "shingles": shingles(key, shingle_n),
                },
            )
            grp["docs"].add(doc_id)
            grp["texts"][raw.strip()] += 1

    # 2. Greedy near-duplicate merge: fold weaker keys into the strongest one
    #    they are similar to. Process by doc-frequency so canonicals win. A
    #    shingle inverted index restricts each comparison to canonicals that
    #    share at least one shingle, keeping this near-linear instead of O(k^2)
    #    over the (many thousands of) distinct block keys in the real corpus.
    order = sorted(groups, key=lambda k: (-len(groups[k]["docs"]), k))
    merged: dict[str, dict] = {}
    shingle_index: dict[str, set[str]] = {}
    for key in order:
        grp = groups[key]
        candidates: set[str] = set()
        for sh in grp["shingles"]:
            candidates |= shingle_index.get(sh, set())
        target = None
        for canon in candidates:
            if _jaccard(grp["shingles"], merged[canon]["shingles"]) >= jaccard:
                target = canon
                break
        if target is None:
            merged[key] = {
                "docs": set(grp["docs"]),
                "texts": Counter(grp["texts"]),
                "shingles": grp["shingles"],
            }
            for sh in grp["shingles"]:
                shingle_index.setdefault(sh, set()).add(key)
        else:
            merged[target]["docs"].update(grp["docs"])
            merged[target]["texts"].update(grp["texts"])

    # 3. Emit records for clusters meeting the evidence threshold.
    records = []
    for key, grp in merged.items():
        evidence = len(grp["docs"])
        if evidence < min_docs:
            continue
        canonical_text = grp["texts"].most_common(1)[0][0]
        records.append(
            {
                "id": _bp_id(key),
                "label": _label(canonical_text),
                "key": key,
                "text": canonical_text,
                "evidence_docs": evidence,
            }
        )

    records.sort(key=lambda r: (-r["evidence_docs"], r["id"]))
    return records
