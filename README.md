# vdocs-spike

Throwaway-quality (but well-tested) exploratory tool that reads the already-normalized
VistA document corpus and, **per `doc_type`**, induces:

1. the recurring **section template** each doc_type was built from, and
2. the recurring verbatim **boilerplate** blocks shared across documents of that type.

This is research, not production — a scouting run to decide what's worth hand-curating into
the real [`vdocs`](../vdocs) `registries/`. Outputs are schema-compatible with
`vdocs/registries/templates` and `vdocs/registries/boilerplate`.

## Input (read-only)

`~/data/vdocs/documents/silver/text/03-normalized/<PKG>/<doc_slug>/body.md` — YAML
frontmatter (`doc_type`, `app_code`, …) → `## Contents` TOC → `##`/`###` body. The corpus
is treated as **read-only**; the spike writes only to `out/`.

## Usage

```bash
make install
.venv/bin/vdocs-spike analyze                 # full 469-doc corpus → out/
.venv/bin/vdocs-spike analyze --doc-type RN   # one doc_type
.venv/bin/vdocs-spike analyze --min-docs 5 --top-boilerplate 30
```

Outputs (`out/`):

- `report.md` — the human deliverable: per-doc_type skeleton, evidence counts, top
  boilerplate, and computed curator caveats.
- `templates-by-doctype.yaml` — `registries/templates`-shaped section schemas.
- `boilerplate-by-doctype.yaml` — `registries/boilerplate`-shaped recurring blocks
  (top-N per doc_type).

## Design

Pure-first, mirroring `vdocs`: zero-I/O transforms in `*_pure.py`, thin I/O drivers separately.

| module | role |
|---|---|
| `parse_pure.py` | split frontmatter, parse TOC, split prose blocks, `block_key`, shingles |
| `templates_pure.py` | induce per-doc_type section skeleton (evidence-scored, ordered) |
| `boilerplate_pure.py` | cluster recurring blocks within a doc_type (exact key + shingle near-dup) |
| `corpus.py` | discover/load `body.md` into `Document`s, group by doc_type (I/O) |
| `analyze.py` | combine induction + clustering per doc_type |
| `report.py` | render registry YAML objects + markdown report (pure) |
| `cli.py` | Typer `analyze` driver (I/O) |

**Template induction** keys sections by `(anchor, level)`, counts `evidence_docs`, orders by
median TOC position, and admits a section only above the evidence floor
`max(min_docs, round(0.2 × n_docs))` — scaling with corpus size so a 120-doc type's one-off
headings are dropped without over-pruning a 4-doc type. `required` = appears in ≥ 50% of docs.

**Boilerplate clustering** groups prose blocks by whitespace-collapsed/lowercased `block_key`,
merges near-duplicates via a shingle inverted index (near-linear, not O(k²)), and keeps clusters
recurring across ≥ `min_docs` distinct documents.

## Findings (469 docs, 24 doc_types)

- **`DIBR` (120 docs) is the one corpus-wide standardized template** — a clean 39-section
  Deployment/Installation/Back-out/Rollback skeleton, every section at 60–94% coverage. Directly
  promotable. Its boilerplate (VA title-page lines, the canonical "This document describes the
  Deployment, Installation, Back-out…" paragraph, KIDS install prompts) is equally clean.
- **Small "strong" cohorts (`API` 8, `CFG` 8, `POM` 5, `AG` 4)** look templated only because a
  handful of near-identical docs manufacture shared structure — verify before promoting.
- **Large heterogeneous types (`IG` 108, `RN` 83, `TM` 42, `UM`, `UG`, `DG`)** have sections but
  none reach 50% coverage: their headings carry numbered/renamed prefixes (`1. Introduction`,
  `2.1 …`) that defeat exact-anchor alignment. Inducing skeletons for these needs **fuzzy heading
  alignment** — out of scope for this spike, flagged for `vdocs` proper.
- **Sparse types (`CVG` 1, `FAQ`/`DESC`/`APX` 2)** can't be induced.

## Develop

```bash
make test     # pytest (fast, -x, random order) + Hypothesis property tests
make check    # ruff + mypy + coverage gate
```
