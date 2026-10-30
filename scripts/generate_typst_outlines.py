"""Regenerate the logo outlines of ``heiglogo.typ`` from ``heiglogo.sty``.

The LaTeX package is the single source of the logo drawings: each vintage is a
``\\heiglogo@draw@<year>`` macro of TikZ ``\\fill`` paths in native units. This
script translates those paths into the Typst data ``heiglogo.typ`` draws from,
and rewrites the block between its ``BEGIN``/``END GENERATED`` markers.

    python scripts/generate_typst_outlines.py          # rewrite heiglogo.typ
    python scripts/generate_typst_outlines.py --check  # fail when out of date

Run it after refreshing ``heiglogo.sty`` from upstream.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRAGMENT = (
    Path(__file__).resolve().parent.parent
    / "src"
    / "texsmith_fragment_heig_logo"
    / "fragment"
)
STY = FRAGMENT / "heiglogo.sty"
TYP = FRAGMENT / "heiglogo.typ"

BEGIN = "// BEGIN GENERATED OUTLINES (scripts/generate_typst_outlines.py)"
END = "// END GENERATED OUTLINES"

# The TikZ colour of a fill, as the role heiglogo.typ resolves to a colour.
_ROLES = {
    r"\heiglogo@curcolor": "ink",
    r"\heiglogo@logocolor": "logo",
    r"\heiglogo@c@a": "a",
    r"\heiglogo@c@b": "b",
    r"\heiglogo@c@c": "c",
    "white": "white",
}

_DRAW = re.compile(
    r"\\expandafter\\def\\csname heiglogo@draw@(\d{4})\\endcsname\{%(.*?)\n\}",
    re.DOTALL,
)
_SETYEAR = re.compile(
    r"\\expandafter\\def\\csname heiglogo@setyear@(\d{4})\\endcsname\{%(.*?)\n\}",
    re.DOTALL,
)
_FILL = re.compile(r"\\fill\[([^\]]*)\]\s*(.*?);", re.DOTALL)
_TOKEN = re.compile(
    r"\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)|(--)|(\.\.controls)|(and)|(\.\.)|(rectangle)|(cycle)"
)
_SETTING = re.compile(r"\\def\\heiglogo@(\w+)\{([^}]*)\}")


def _number(text: str) -> str:
    value = float(text)
    return str(int(value)) if value.is_integer() else repr(value)


def parse_path(path: str) -> list[tuple[str, ...]]:
    """Translate one TikZ path into ``M``/``L``/``C``/``Z`` segments."""
    segments: list[tuple[str, ...]] = []
    pending: str | None = None  # the connector waiting for its point(s)
    controls: list[tuple[str, str]] = []
    start: tuple[str, str] | None = None
    current: tuple[str, str] | None = None
    for match in _TOKEN.finditer(path):
        x, y, line, curve, _and, _dots, rectangle, cycle = match.groups()
        if x is not None:
            point = (_number(x), _number(y))
            if pending == "--":
                segments.append(("L", *point))
            elif pending == "controls":
                controls.append(point)
                if len(controls) < 3:
                    continue
                segments.append(("C", *controls[0], *controls[1], *controls[2]))
                controls = []
            elif pending == "rectangle":
                assert current is not None
                (x0, y0), (x1, y1) = current, point
                segments += [("L", x1, y0), ("L", x1, y1), ("L", x0, y1), ("Z",)]
            else:
                segments.append(("M", *point))
                start = point
            pending = None
            current = point
        elif line:
            pending = "--"
        elif curve:
            pending = "controls"
        elif rectangle:
            pending = "rectangle"
        elif cycle:
            segments.append(("Z",))
            pending = None
            current = start
    return segments


def _typst_segment(segment: tuple[str, ...]) -> str:
    return (
        "("
        + ", ".join([f'"{segment[0]}"', *segment[1:]])
        + ("," if len(segment) == 1 else "")
        + ")"
    )


def vintages(sty: str) -> dict[str, dict[str, object]]:
    """The geometry and the fills of every vintage of ``sty``."""
    settings = {
        year: dict(_SETTING.findall(body)) for year, body in _SETYEAR.findall(sty)
    }
    result: dict[str, dict[str, object]] = {}
    for year, body in _DRAW.findall(sty):
        fills = []
        for options, path in _FILL.findall(body):
            parts = [part.strip() for part in options.split(",")]
            fills.append(
                {
                    "role": _ROLES[parts[0]],
                    "even_odd": "even odd rule" in parts,
                    "path": parse_path(path),
                }
            )
        result[year] = {"settings": settings[year], "fills": fills}
    return result


def render(sty: str) -> str:
    """The Typst block between the markers."""
    lines = [
        BEGIN,
        "// Do not edit: translated from the \\heiglogo@draw@<year> macros.",
        "#let _vintages = (",
    ]
    for year, data in vintages(sty).items():
        settings = data["settings"]
        lines.append(f'  "{year}": (')
        lines.append(
            f"    width: {settings['nativewidth']}, height: {settings['nativeheight']}, "
            f"separator: {settings['separatorx']}, text: {settings['textanchorx']},"
        )
        lines.append(f'    size: ("{settings["defsizemode"]}", {settings["defsize"]}),')
        lines.append("    fills: (")
        for fill in data["fills"]:  # type: ignore[union-attr]
            path = ", ".join(_typst_segment(segment) for segment in fill["path"])
            even_odd = "true" if fill["even_odd"] else "false"
            lines.append(
                f'      (role: "{fill["role"]}", even-odd: {even_odd}, path: ({path},)),'
            )
        lines.append("    ),")
        lines.append("  ),")
    lines += [")", END]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check", action="store_true", help="fail when heiglogo.typ is out of date"
    )
    args = parser.parse_args()

    typ = TYP.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(typ):
        print(f"{TYP}: generated-block markers not found", file=sys.stderr)
        return 1
    updated = pattern.sub(lambda _: render(STY.read_text(encoding="utf-8")), typ)
    if args.check:
        if updated != typ:
            print(f"{TYP} is out of date; run {Path(__file__).name}", file=sys.stderr)
            return 1
        return 0
    TYP.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
