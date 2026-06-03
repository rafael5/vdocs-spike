"""Tests for the Typer CLI driver (real tmp corpus, real output files)."""

from pathlib import Path

import yaml
from typer.testing import CliRunner

from vdocs_spike.cli import app

runner = CliRunner()

DOC = """---
doc_type: RN
app_code: PSO
---

# Release Notes {n}

## Contents

- [Overview](#overview)

## Overview

A shared boilerplate paragraph present in every release note document here.
"""


def _corpus(tmp_path: Path, n: int = 3) -> Path:
    root = tmp_path / "corpus"
    for i in range(n):
        d = root / "PSO" / f"doc_{i}"
        d.mkdir(parents=True)
        (d / "body.md").write_text(DOC.format(n=i))
    return root


def test_analyze_writes_outputs(tmp_path):
    root = _corpus(tmp_path)
    out = tmp_path / "out"
    result = runner.invoke(
        app, ["analyze", "--root", str(root), "--out", str(out), "--min-docs", "2"]
    )
    assert result.exit_code == 0, result.output
    assert (out / "report.md").exists()
    assert (out / "templates-by-doctype.yaml").exists()
    assert (out / "boilerplate-by-doctype.yaml").exists()

    tpl = yaml.safe_load((out / "templates-by-doctype.yaml").read_text())
    assert tpl["templates"][0]["doc_type"] == "RN"
    bp = yaml.safe_load((out / "boilerplate-by-doctype.yaml").read_text())
    assert bp["boilerplate"][0]["evidence_docs"] == 3


def test_analyze_doc_type_filter(tmp_path):
    root = _corpus(tmp_path)
    out = tmp_path / "out"
    result = runner.invoke(
        app,
        [
            "analyze",
            "--root",
            str(root),
            "--out",
            str(out),
            "--doc-type",
            "ZZ",
            "--min-docs",
            "2",
        ],
    )
    assert result.exit_code == 0, result.output
    # No docs of type ZZ -> empty registries.
    tpl = yaml.safe_load((out / "templates-by-doctype.yaml").read_text())
    assert tpl["templates"] == []


def test_analyze_missing_root_errors(tmp_path):
    result = runner.invoke(
        app, ["analyze", "--root", str(tmp_path / "nope"), "--out", str(tmp_path / "o")]
    )
    assert result.exit_code != 0
