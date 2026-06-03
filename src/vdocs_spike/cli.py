"""Typer CLI: induce per-doc_type templates and boilerplate from the corpus."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import typer
import yaml

from vdocs_spike.analyze import analyze_all
from vdocs_spike.corpus import group_by_doc_type, load_corpus
from vdocs_spike.report import (
    boilerplate_yaml_obj,
    render_report,
    templates_yaml_obj,
)

DEFAULT_ROOT = Path.home() / "data/vdocs/documents/silver/text/03-normalized"

app = typer.Typer(
    add_completion=False,
    help="Induce section templates and boilerplate from the normalized VistA corpus.",
)


@app.callback()
def _root() -> None:
    """vdocs-spike — exploratory template & boilerplate induction."""


def _dump_yaml(obj: dict, path: Path) -> None:
    path.write_text(
        yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


@app.command()
def analyze(
    root: Path = typer.Option(
        DEFAULT_ROOT, "--root", help="Normalized corpus root (read-only)."
    ),
    out: Path = typer.Option(
        Path("out"), "--out", help="Output directory for registries + report."
    ),
    doc_type: Optional[str] = typer.Option(
        None, "--doc-type", help="Restrict analysis to a single doc_type."
    ),
    min_docs: int = typer.Option(
        3, "--min-docs", help="Min distinct docs for a section/block to count."
    ),
    top_boilerplate: int = typer.Option(
        50, "--top-boilerplate", help="Max boilerplate blocks per doc_type in YAML."
    ),
) -> None:
    """Run the induction and write registries + report to ``--out``."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if not root.exists():
        typer.secho(f"corpus root not found: {root}", fg="red", err=True)
        raise typer.Exit(code=1)

    docs = load_corpus(root)
    grouped = group_by_doc_type(docs)
    if doc_type is not None:
        grouped = {doc_type: grouped.get(doc_type, [])}

    analyses = analyze_all(grouped, min_docs=min_docs)

    out.mkdir(parents=True, exist_ok=True)
    _dump_yaml(templates_yaml_obj(analyses), out / "templates-by-doctype.yaml")
    _dump_yaml(
        boilerplate_yaml_obj(analyses, top_n=top_boilerplate),
        out / "boilerplate-by-doctype.yaml",
    )
    (out / "report.md").write_text(
        render_report(analyses, min_docs=min_docs), encoding="utf-8"
    )

    n_tpl = len(templates_yaml_obj(analyses)["templates"])
    n_bp = len(boilerplate_yaml_obj(analyses, top_n=top_boilerplate)["boilerplate"])
    typer.secho(
        f"analyzed {len(docs)} docs / {len(analyses)} doc_types → "
        f"{n_tpl} templates, {n_bp} boilerplate blocks. wrote {out}/",
        fg="green",
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
