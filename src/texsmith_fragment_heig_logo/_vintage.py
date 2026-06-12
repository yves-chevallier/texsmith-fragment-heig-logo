"""Resolve which HEIG-VD logo *vintage* a document should use.

The upstream ``heiglogo`` LaTeX package (https://github.com/HEIG-VD/logos)
ships four logo vintages, selected through the ``year`` key of ``\\logo``:
``1998``, ``2004``, ``2009`` and ``2020`` (the current letterhead).

A document can pick a vintage in two ways:

* **Explicitly**, via the ``heiglogo.year`` front-matter attribute; or
* **Automatically**, by leaving ``heiglogo.year`` on its default (``"auto"``),
  in which case the vintage is derived from the document ``date`` — a paper
  written in, say, 2006 gets the 2004 logo that was in force at the time.

This module holds the pure, dependency-free logic so it can be unit-tested
without a TeXSmith runtime.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any

__all__ = [
    "VINTAGES",
    "LATEST_VINTAGE",
    "extract_year",
    "vintage_for_year",
    "resolve_vintage",
]

# Known logo vintages, in chronological order. The value is both the public
# identifier and the ``year`` option understood by the LaTeX package.
VINTAGES: tuple[str, ...] = ("1998", "2004", "2009", "2020")

# Default when no date is available: the current letterhead.
LATEST_VINTAGE: str = "2020"

# Each vintage stays in force from the year it was introduced until the next
# one appears, so the identifier doubles as its introduction year.
_INTRODUCED: dict[str, int] = {vintage: int(vintage) for vintage in VINTAGES}

# A standalone four-digit run, used to recover the year from an already
# formatted date string such as "5 mars 2026" or "March 5, 2026".
_YEAR_RE = re.compile(r"(?<!\d)(\d{4})(?!\d)")


def vintage_for_year(year: int) -> str:
    """Return the logo vintage in force during calendar ``year``.

    Years before the first vintage fall back to the oldest one.
    """
    selected = VINTAGES[0]
    for vintage in VINTAGES:
        if year >= _INTRODUCED[vintage]:
            selected = vintage
        else:
            break
    return selected


def extract_year(date_value: Any, *, today: date | None = None) -> int | None:
    """Best-effort extraction of a four-digit year from a front-matter date.

    Handles ``date``/``datetime`` objects, plain integers, ISO strings and the
    long-form strings TeXSmith produces once a template has localised the date
    (e.g. ``"5 mars 2026"``). The ``"today"`` keyword resolves to ``today``'s
    year (injectable for deterministic tests). Anything unrecognised yields
    ``None`` so the caller can fall back to a default vintage.
    """
    if date_value is None or isinstance(date_value, bool):
        return None
    if isinstance(date_value, datetime):
        return date_value.year
    if isinstance(date_value, date):
        return date_value.year
    if isinstance(date_value, int):
        return date_value if 1000 <= date_value <= 9999 else None

    text = str(date_value).strip()
    if not text:
        return None
    if text.lower() == "today":
        return (today or date.today()).year  # noqa: DTZ011 - date source is the caller's concern
    match = _YEAR_RE.search(text)
    return int(match.group(1)) if match else None


def resolve_vintage(
    explicit: Any,
    date_value: Any = None,
    *,
    default: str = LATEST_VINTAGE,
    today: date | None = None,
) -> str:
    """Resolve the logo vintage from an explicit setting or the document date.

    An ``explicit`` value naming a known vintage always wins. ``None``, the
    empty string and ``"auto"`` (case-insensitive) defer to ``date_value``; if
    no usable year is found there, ``default`` is returned.

    Raises:
        ValueError: when ``explicit`` names an unknown vintage.
    """
    token = "" if explicit is None else str(explicit).strip().lower()
    if token and token != "auto":
        if token in _INTRODUCED:
            return token
        raise ValueError(
            f"Unknown heiglogo year {explicit!r}; expected one of "
            f"{', '.join(VINTAGES)} or 'auto'."
        )

    year = extract_year(date_value, today=today)
    if year is None:
        return default
    return vintage_for_year(year)
