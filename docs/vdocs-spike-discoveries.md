# vdocs-spike — discoveries

**Status:** research deliverable from the `vdocs-spike` scouting run (June 2026).
**Audience:** whoever implements the `discover` stage + registries in [`vdocs`](https://github.com/rafael5/vdocs).
**Companion:** the implementation work order is `vdocs/docs/prompts/vdocs-spike-implement-discoveries.md`.

This document records (1) what the spike found in the real 469-document corpus, (2) how it found
it, and (3) exactly where this capability belongs in the `vdocs` 17-stage pipeline and what must
change to make it production-grade. It is the bridge between a throwaway prototype and the real
`discover` stage.

---

## 1. What the spike is

A small, TDD'd, pure-first tool that reads the already-normalized corpus
(`~/data/vdocs/documents/silver/text/03-normalized/<PKG>/<slug>/body.md`) and, **per `doc_type`**,
induces two things:

1. the recurring **section template** each doc_type was poured into, and
2. the recurring verbatim **boilerplate** blocks shared across documents of that type.

It emits registry-shaped YAML (`templates-by-doctype.yaml`, `boilerplate-by-doctype.yaml`) plus a
human report (`report.md`). It mutates nothing — it only *proposes*. Modules mirror the `vdocs`
discipline (zero-I/O `*_pure.py` + thin I/O drivers, Hypothesis property tests):

| module | role |
|---|---|
| `parse_pure` | split frontmatter, parse `## Contents` TOC, split prose blocks, `block_key`, shingles |
| `templates_pure` | induce per-doc_type section skeleton (evidence-scored, ordered by median TOC position) |
| `boilerplate_pure` | cluster recurring blocks within a doc_type (exact key + shingle near-dup merge) |
| `corpus` / `analyze` / `report` / `cli` | discover & load `body.md`, combine, render, drive (Typer `analyze`) |

---

## 2. Findings (469 docs, 24 doc_types, `--min-docs 3`)

11 templates and 534 boilerplate candidates (top-50/type) were induced. The doc_types sort into
four tiers by the strength of their induced **required** skeleton (a section is *required* when it
appears in ≥ 50% of the type's docs):

| Tier | doc_types | Reading |
|---|---|---|
| **Strong, promotable** | `DIBR` (120 docs → 39 sections, all required) | Corpus-wide standardized template. Promote. |
| **Strong but small-cohort (verify)** | `API` (8), `CFG` (8), `POM` (5), `AG` (4) | "Strong" only because a handful of near-identical docs manufacture shared structure. `API`'s 256-section result is a heading *dump*, not a template; `CFG`/`AG`/`POM` worth a human look. |
| **Heterogeneous (sections found, none required)** | `IG` (108, 0 sections), `RN` (83), `TM` (42), `UM` (25), `UG` (14), `DG` (12) | Real shared structure exists but exact-anchor alignment can't see it — numbered/renamed heading slugs (`1. Introduction`, `2.1 …`) never align. **The single biggest miss; see §5.** |
| **Sparse** | `CVG` (1), `APX`/`DESC`/`FAQ` (2) | Too few docs to induce anything. Correctly skipped. |

### 2.1 DIBR validates the method

The spike's induced `DIBR` template — *Purpose, Dependencies, Constraints, Timeline, Site Readiness
Assessment, Deployment Topology, Site Information, Site Preparation, Resources, Facility Specifics,
Hardware, Software, Communications, … , Back-Out/Rollback Strategy/Considerations/Criteria/Risks/
Authority/Procedure/Verification* — **matches the already hand-curated
`vdocs/registries/templates/templates.yaml` DIBR template almost section-for-section**, at 60–94%
per-section coverage. The two were produced independently; their agreement is strong evidence the
induction approach is sound. The DIBR boilerplate is equally clean: VA title-page lines
("Department of Veterans Affairs", "Office of Information and Technology (OIT)"), the canonical
"This document describes the Deployment, Installation, Back-out…" paragraph, and the KIDS install
prompts — the same blocks already in `registries/boilerplate`.

### 2.2 Boilerplate is the broadly-useful half

Even for the heterogeneous types that yield no template, boilerplate clustering still produces
clean, curation-worthy blocks (e.g. `TM` surfaced 768 candidates, `DG` 393). Boilerplate
subtraction does **not** depend on a document type having a coherent skeleton, so it pays off across
far more of the corpus than template induction does.

---

## 3. How it works (the methods worth porting)

**Template induction** (`templates_pure.induce_template`): key each section by `(anchor_slug, level)`;
count `evidence_docs` (distinct docs containing it); order by **median TOC position**; admit a
section only above the evidence floor `max(min_docs, round(0.2 × n_docs))` — the ratio term scales
the floor with corpus size so a 120-doc type's one-off headings drop without over-pruning a 4-doc
type. `required` = appears in ≥ 50% of docs. This evidence floor is what collapsed an initial noisy
168-section DIBR result down to the clean 39-section skeleton.

**Boilerplate clustering** (`boilerplate_pure.cluster_boilerplate`): split each body into prose
blocks (markdown artifacts — nav links, secondary TOC lines, `<img>` tags, table-CSV markers — are
dropped first); group by `block_key` (whitespace-collapsed, lowercased — the exact match identity
that the registry's `key` field uses); merge near-duplicates via a **shingle inverted index** (only
compare blocks that share a 4-gram shingle, keeping it near-linear instead of O(k²) over the
thousands of distinct keys); keep clusters recurring across ≥ `min_docs` distinct documents; emit
`{id, label, key, text, evidence_docs}` sorted by evidence.

Both are deterministic and stable (template_id / bp-id are content hashes), which matters for a
re-runnable miner.

---

## 4. Where this fits in `vdocs` — it is the `discover` stage

This is not a new stage. It is a prototype of the existing **`discover`** stage (§8, silver·DOC,
**Phase 3** of §17), specifically its template + boilerplate miners. The design names the v1
detectors it promotes: *"the miners are the promoted v1 detectors (`boilerplate_pure`, `lexicon`,
`headings`)"* (§9.6).

The load-bearing rule is the **induction ↔ application split** (§9.6). `discover` is corpus-global,
statistical, and adaptive; it only *proposes*. Everything that touches a document body is per-doc,
pure, and deterministic, and lives in a *different* stage:

```
discover ─► candidate patterns ─► CURATE (gate) ─► registries/ ─► normalize subtracts & references
(mine)      reports/patterns/      auto / human PR   the seam       pure fn of (document × registry)
     ▲                                                                       │
     └─────────────────── re-discover on drift / new era ◄──────────────────┘
```

The spike does only the **left half** (induce → propose registry-shaped YAML). The three benefits
that motivate this work are each delivered by a *downstream* stage that consumes the curated
registry:

| Benefit | Delivered by | Design reference |
|---|---|---|
| Validate TOC + section headings against the known skeleton | **`fidelity`** (Phase 5) + the `validate` hard gate | §9.8 template-compliance oracle; fidelity scores template compliance + TOC integrity |
| Reframe/restructure each doc around its master template | **`normalize`** (Phase 3) | `registries/templates` disposition = **STRIP + STAMP + RETAIN**; TOC regenerated from headings (§6.7) |
| Subtract repeated boilerplate → shrink to unique content → cleaner search | **`normalize`** applies it; payoff realized in **`index`/`embed`** | `registries/boilerplate` = **REFERENCE** to `gold/_shared/`; anchor-only clean search surface (ADR-021, §14.6) |

So the data path the spike feeds is:
**`discover` (mine) → curation gate → `registries/{templates,boilerplate}` → `normalize` (apply) →
`fidelity`/`validate` (check) → `index`/`embed` (clean retrieval).** This is why the spike's YAML
was deliberately shaped to be schema-compatible with both registries — its output is meant to be
hand-merged through that curation gate.

### 4.1 Keep this straight

The miner must **never strip**. The whole reason for the seam is that `normalize` stays a *pure
function of `(document, registry)`* — same registries in, same body out (§7.4). The spike proposing
a 39-section DIBR skeleton is correct; a miner rewriting a body would violate the architecture.
Induction is adaptive and statistical; application is deterministic and per-doc; they are
deliberately different homes.

---

## 5. Gaps between the spike and production `discover`

Three deltas, in priority order. The first explains most of the spike's "heterogeneous" misses.

1. **Add the `era` axis — highest value.** Production templates are keyed by **`(doc_type, era)`**,
   not `doc_type` alone — *"different skeletons in the 1990s, 2000s, 2010s"* (§9.6); era = the
   title-page publication date bucketed by decade. The spike collapsed era, and that is almost
   certainly why **`DIBR` induced a clean template (it's a recent, single-era VIP standard) while
   `IG`/`RN`/`TM`/`UG`/`DG` came out "heterogeneous, none required."** Those big types are very
   likely *several per-era templates blurred together* — the existing curated registry already has
   both `DIBR:2010s` and `DIBR:2020s`. Splitting on era should convert much of that "noise" into
   real per-era skeletons. **This is the single most important upgrade.**

2. **Enrich the schema to §9.8.** A production template section is a *computable structural schema*:
   `{section_id, title-pattern, heading-level, required|optional, repeatable, semantic_role,
   toc_level}` plus expected markers (TOC resolves to headings, revision-history block, numbering
   scheme). The spike emits `{section_id, title, level, required, toc_level, evidence_docs}` — close,
   but missing `title-pattern` (a regex, since titles vary), `semantic_role`, and `repeatable`. A
   `title-pattern` derived by clustering near-identical titles would *also* help the heterogeneous
   alignment problem in (1) by aligning `Introduction` / `1. Introduction` / `1 Introduction`.

3. **Read `text@converted`, not `03-normalized`.** Production `discover` runs one medallion step
   earlier (pre-normalize, on converted text) and is corpus-global. The spike read normalized text
   for convenience; fine for scouting, but the real miner mines `text@converted` and takes
   `doc_code` from `catalog.enriched` (the authoritative doc_type — classification stays a `catalog`
   decision, not re-derived).

Lesser notes: production boilerplate identity uses shingle/MinHash from `kernel/discovery/` (the
spike's shingle index is a compatible but simpler take); candidates must be emitted to
`reports/patterns/` **with a proposed disposition + evidence** for the curation gate, not written
straight into `registries/`.

---

## 6. Recommended promotions (what to hand-merge now, before the rebuild)

- **`DIBR` template** — already validated against the curated registry; any new sections the spike
  surfaced are low-risk additions.
- **Boilerplate across `DIBR`, `IG`, `TM`, `DG`** — the top-evidence blocks (VA title-page furniture,
  the DIBR/CAPRI description paragraphs, KIDS install prompts, standard table captions) are clean and
  type-tagged; promote the high-evidence head of each list.
- **Hold** the small-cohort "strong" templates (`API`, `CFG`, `POM`, `AG`) pending a human look —
  `CFG`/`AG` are plausible, `API` is a dump.
- **Defer** `RN`/`IG`/`TM`/`UG`/`DG` templates until the era axis (§5.1) is added — re-mine with
  `(doc_type, era)` first; their *boilerplate* is promotable now regardless.

---

## Appendix — reproducing

```bash
cd ~/projects/vdocs-spike && make install
.venv/bin/vdocs-spike analyze --min-docs 3        # full corpus → out/
```

Outputs: `out/report.md` (human deliverable), `out/templates-by-doctype.yaml`,
`out/boilerplate-by-doctype.yaml` (both registry-schema-compatible). Repo:
<https://github.com/rafael5/vdocs-spike>.
