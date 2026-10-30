"""The HEIG-VD institutes and centres whose logo carries a text block.

The 2020 graphic charter (*Logothèque*, pages 17 and 18) gives each of the
eight institutes and four centres a logo made of the HEIG-VD mark, a vertical
bar and a text block:

* an **institute** shows its acronym in bold on the first line and its full
  name, in regular weight, flush with the bottom of the mark;
* a **centre** shows its whole name in bold, from the top.

The charter sets the text in Circular, which is not freely available, so the
LaTeX and Typst renderings use Arial (with metric-compatible fallbacks).

The line breaks below are those of the charter; they are kept verbatim rather
than left to the paragraph builder so that every logo reads as in the charter.
Like :mod:`._vintage`, this module is dependency-free so it can be unit-tested
without a TeXSmith runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = ["GROUPS", "Group", "latex_text", "resolve_group"]


@dataclass(frozen=True, slots=True)
class Group:
    """One institute or centre logo: the bold title and the regular subtitle."""

    key: str
    title: tuple[str, ...]
    subtitle: tuple[str, ...] = ()


GROUPS: dict[str, Group] = {
    group.key: group
    for group in (
        # Instituts
        Group(
            "comatec",
            ("COMATEC",),
            ("Institut de Conception", "mécanique et", "Technologies des", "matériaux"),
        ),
        Group("iai", ("IAI",), ("Institut", "d’Automatisation", "industrielle")),
        Group("ie", ("IE",), ("Institut", "des Énergies")),
        Group(
            "iict",
            ("IICT",),
            (
                "Institut des",
                "Technologies de",
                "l’information et de",
                "la communication",
            ),
        ),
        Group(
            "iide",
            ("IIDE",),
            ("Institut", "interdisciplinaire", "du Développement", "de l’entreprise"),
        ),
        Group("insit", ("INSIT",), ("Institut", "d’Ingénierie", "du territoire")),
        Group("mei", ("MEI",), ("Media", "Engineering", "Institute")),
        Group(
            "reds",
            ("REDS",),
            ("Institut", "Reconfigurable", "and Embedded", "Digital Systems"),
        ),
        # Centres
        Group("formation-continue", ("Centre", "Formation", "continue")),
        Group("formation-base", ("Centre", "Formation", "de base")),
        Group("rad", ("Centre", "Ra&D")),
        Group("relations-internationales", ("Centre", "Relations", "internationales")),
    )
}

# Spellings that name no group: the logo is then drawn without text.
_NONE = {"", "none", "false", "no", "off"}

_LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def resolve_group(value: Any) -> Group | None:
    """Return the group named by ``value``, or ``None`` for a logo without text.

    The name is case-insensitive and tolerates underscores and spaces for
    hyphens (``Formation_continue``, ``formation continue``).

    Raises:
        ValueError: when ``value`` names no known group.
    """
    if value is None or value is False:
        return None
    token = str(value).strip().lower().replace("_", "-").replace(" ", "-")
    if token in _NONE:
        return None
    group = GROUPS.get(token)
    if group is None:
        raise ValueError(
            f"Unknown heiglogo group {value!r}; expected one of {', '.join(GROUPS)}."
        )
    return group


def latex_text(lines: tuple[str, ...]) -> str:
    """Join ``lines`` as LaTeX source, one ``\\\\``-separated line each."""
    return r"\\".join(
        "".join(_LATEX_SPECIALS.get(char, char) for char in line) for line in lines
    )
