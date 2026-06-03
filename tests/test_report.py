"""Tests for pure report + registry-YAML rendering."""

import yaml

from vdocs_spike.report import (
    boilerplate_yaml_obj,
    render_report,
    templates_yaml_obj,
)

ANALYSES = [
    {
        "doc_type": "RN",
        "n_docs": 3,
        "sparse": False,
        "template": {
            "template_id": "RN:abcd1234",
            "doc_type": "RN",
            "evidence_docs": 3,
            "sections": [
                {
                    "section_id": "intro",
                    "title": "Intro",
                    "level": 2,
                    "required": True,
                    "toc_level": True,
                    "evidence_docs": 3,
                }
            ],
        },
        "boilerplate": [
            {
                "id": "bp-deadbeef00",
                "label": "Shared block",
                "key": "shared block text",
                "text": "Shared block text",
                "evidence_docs": 3,
                "doc_type": "RN",
            }
        ],
    },
    {
        "doc_type": "CVG",
        "n_docs": 1,
        "sparse": True,
        "template": {
            "template_id": "CVG:0000",
            "doc_type": "CVG",
            "evidence_docs": 1,
            "sections": [],
        },
        "boilerplate": [],
    },
]


def test_templates_yaml_obj_excludes_sparse_and_empty():
    obj = templates_yaml_obj(ANALYSES)
    ids = [t["template_id"] for t in obj["templates"]]
    assert ids == ["RN:abcd1234"]  # CVG sparse + empty excluded


def test_boilerplate_yaml_obj_flattens_all_records():
    obj = boilerplate_yaml_obj(ANALYSES)
    assert len(obj["boilerplate"]) == 1
    assert obj["boilerplate"][0]["id"] == "bp-deadbeef00"


def test_boilerplate_yaml_obj_caps_top_n_per_doctype():
    analyses = [
        {
            "doc_type": "DIBR",
            "n_docs": 100,
            "sparse": False,
            "template": {"sections": []},
            "boilerplate": [
                {
                    "id": f"bp-{i:04d}",
                    "label": "x",
                    "key": f"k{i}",
                    "text": "x",
                    "evidence_docs": 100 - i,
                    "doc_type": "DIBR",
                }
                for i in range(200)
            ],
        }
    ]
    obj = boilerplate_yaml_obj(analyses, top_n=50)
    assert len(obj["boilerplate"]) == 50
    # Kept the highest-evidence ones (already sorted desc within a doc_type).
    assert obj["boilerplate"][0]["id"] == "bp-0000"
    assert obj["boilerplate"][-1]["evidence_docs"] == 51


def test_yaml_objs_round_trip_serializable():
    # Must serialize cleanly so outputs are valid registry YAML.
    t = yaml.safe_dump(templates_yaml_obj(ANALYSES))
    b = yaml.safe_dump(boilerplate_yaml_obj(ANALYSES))
    assert "RN:abcd1234" in t
    assert "bp-deadbeef00" in b


def test_render_report_has_per_doctype_sections_and_sparse_notes():
    md = render_report(ANALYSES, min_docs=3)
    assert "# " in md  # has a title
    assert "RN" in md
    assert "Intro" in md  # template section listed
    assert "Shared block" in md  # boilerplate listed
    assert "CVG" in md
    assert "sparse" in md.lower()  # sparse note present
    assert "3" in md  # evidence counts shown
    assert "Notes" in md  # curator caveats section present


def test_render_report_flags_small_cohort_strong():
    analyses = [
        {
            "doc_type": "API",
            "n_docs": 8,
            "sparse": False,
            "template": {
                "template_id": "API:x",
                "doc_type": "API",
                "evidence_docs": 8,
                "sections": [
                    {
                        "section_id": f"s{i}",
                        "title": f"S{i}",
                        "level": 2,
                        "required": True,
                        "toc_level": True,
                        "evidence_docs": 6,
                    }
                    for i in range(6)
                ],
            },
            "boilerplate": [],
        }
    ]
    md = render_report(analyses, min_docs=3)
    # Small-cohort strong types should be flagged as needing verification.
    assert "API" in md
    assert "small" in md.lower()
