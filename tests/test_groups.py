"""Tests for the institute and centre table, and its Typst mirror."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

from texsmith_fragment_heig_logo import FRAGMENT_PATH
from texsmith_fragment_heig_logo._groups import GROUPS, latex_text, resolve_group


def test_twelve_groups() -> None:
    assert len(GROUPS) == 12
    institutes = [group for group in GROUPS.values() if group.subtitle]
    assert len(institutes) == 8
    assert all(len(group.title) == 1 for group in institutes)


@pytest.mark.parametrize("raw", [None, False, "", "  ", "none", "None", "false"])
def test_no_group(raw: object) -> None:
    assert resolve_group(raw) is None


@pytest.mark.parametrize(
    ("raw", "key"),
    [
        ("reds", "reds"),
        ("REDS", "reds"),
        (" Formation_continue ", "formation-continue"),
        ("relations internationales", "relations-internationales"),
    ],
)
def test_spellings(raw: str, key: str) -> None:
    group = resolve_group(raw)
    assert group is not None
    assert group.key == key


def test_unknown_group() -> None:
    with pytest.raises(ValueError, match="expected one of comatec"):
        resolve_group("heig")


def test_latex_text_escapes_and_breaks() -> None:
    assert latex_text(("Centre", "Ra&D")) == r"Centre\\Ra\&D"
    assert latex_text(("50% #1",)) == r"50\% \#1"


def test_typst_table_mirrors_python() -> None:
    source = (FRAGMENT_PATH / "heiglogo.typ").read_text(encoding="utf-8")
    entries = re.findall(
        r'^  "([a-z-]+)": \(title: \((.*?)\), subtitle: \((.*?)\)\),$',
        source,
        flags=re.MULTILINE,
    )

    def items(text: str) -> tuple[str, ...]:
        return tuple(re.findall(r'"([^"]*)"', text))

    typst = {key: (items(title), items(subtitle)) for key, title, subtitle in entries}
    python = {key: (group.title, group.subtitle) for key, group in GROUPS.items()}
    assert typst == python


def test_typst_outlines_are_generated_from_the_sty() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "scripts"
        / "generate_typst_outlines.py"
    )
    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
