"""The object-oriented HEIG-VD logo fragment.

Kept separate from the package ``__init__`` so that importing the package does
not pull in TeXSmith at module load time. TeXSmith builds its fragment registry
*while* it is being imported and, as part of that, loads this package's entry
point; importing the heavy machinery eagerly here would create a circular
import. The entry point is the lazy factory :func:`.load_fragment`.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar

from texsmith.core.coerce import coerce_bool
from texsmith.core.fragments.base import BaseFragment, FragmentPiece
from texsmith.core.templates.manifest import TemplateAttributeSpec
from texsmith.diagnostics import DiagnosticEmitter

from ._vintage import LATEST_VINTAGE, VINTAGES, resolve_vintage

FRAGMENT_PATH: Path = Path(__file__).resolve().parent / "fragment"

__all__ = ["HeigLogoConfig", "HeigLogoFragment"]

DEFAULT_OFFSET = "1cm"

# The offsets are written verbatim into the LaTeX source: only a plain TeX
# length (a number and a unit) gets through.
_LENGTH = re.compile(r"-?(\d+(\.\d*)?|\.\d+)\s*(pt|mm|cm|in|bp|pc|dd|cc|sp|em|ex)")


def _coerce_bool(value: Any, *, default: bool = False) -> bool:
    """Interpret a front-matter value as a boolean, tolerating strings.

    TeXSmith owns the spelling of a boolean written as text
    (:func:`texsmith.core.coerce.coerce_bool`); ``None`` there means "absent
    or not a boolean", which is this fragment's ``default``.
    """
    resolved = coerce_bool(value)
    return default if resolved is None else resolved


def _coerce_length(value: Any, *, name: str) -> str:
    """Return ``value`` as a TeX length, ``1cm`` when absent."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return DEFAULT_OFFSET
    length = str(value).strip()
    if not _LENGTH.fullmatch(length):
        raise ValueError(
            f"Invalid heiglogo {name} {length!r}: expected a TeX length such as 17mm"
        )
    return length


class HeigLogoConfig:
    """Resolved fragment options handed to the Jinja template."""

    __slots__ = ("color", "left", "top", "year")

    def __init__(
        self,
        *,
        color: bool,
        year: str,
        left: str = DEFAULT_OFFSET,
        top: str = DEFAULT_OFFSET,
    ) -> None:
        self.color = color
        self.year = year
        self.left = left
        self.top = top

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"HeigLogoConfig(color={self.color!r}, year={self.year!r}, "
            f"left={self.left!r}, top={self.top!r})"
        )


class HeigLogoFragment(BaseFragment[HeigLogoConfig]):
    """HEIG-VD letterhead logo with selectable vintage."""

    name: ClassVar[str] = "heiglogo"
    description: ClassVar[str] = (
        "Logo HEIG-VD sur la première page, en haut à gauche, à 1cm des bords "
        "par défaut."
    )
    pieces: ClassVar[list[FragmentPiece]] = [
        FragmentPiece(
            template_path=FRAGMENT_PATH / "heiglogo.sty",
            kind="package",
            output_name="heiglogo",
        ),
        FragmentPiece(
            template_path=FRAGMENT_PATH / "heiglogo.jinja.tex",
            kind="inline",
            # 0.7 renamed ``FragmentPiece.slot`` to ``variable``: a slot is a
            # region a document is assigned to, a variable an injection point.
            variable="extra_packages",
        ),
    ]
    attributes: ClassVar[dict[str, TemplateAttributeSpec]] = {
        "heiglogo_color": TemplateAttributeSpec(
            default=False,
            type="boolean",
            sources=["heiglogo.color", "heiglogo_color"],
            description="Afficher le logo en couleur (rouge HEIG-VD).",
        ),
        "heiglogo_year": TemplateAttributeSpec(
            default="auto",
            sources=["heiglogo.year", "heiglogo_year"],
            description=(
                "Millésime du logo : auto (depuis la date du document), "
                + ", ".join(VINTAGES)
                + "."
            ),
        ),
        "heiglogo_left": TemplateAttributeSpec(
            default=DEFAULT_OFFSET,
            format="raw",
            sources=["heiglogo.left", "heiglogo_left"],
            description=(
                "Distance du logo au bord gauche de la feuille, par exemple 17mm "
                "pour ménager une gouttière de reliure."
            ),
        ),
        "heiglogo_top": TemplateAttributeSpec(
            default=DEFAULT_OFFSET,
            format="raw",
            sources=["heiglogo.top", "heiglogo_top"],
            description="Distance du logo au bord supérieur de la feuille.",
        ),
    }
    config_cls: ClassVar[type[HeigLogoConfig]] = HeigLogoConfig
    source: ClassVar[Path] = FRAGMENT_PATH
    context_defaults: ClassVar[dict[str, Any]] = {
        "heiglogo_color": False,
        "heiglogo_year": LATEST_VINTAGE,
        "heiglogo_left": DEFAULT_OFFSET,
        "heiglogo_top": DEFAULT_OFFSET,
    }

    def build_config(
        self,
        context: Mapping[str, Any],
        overrides: Mapping[str, Any] | None = None,
        *,
        emitter: DiagnosticEmitter | None = None,
    ) -> HeigLogoConfig:
        _ = overrides
        _ = emitter
        color = _coerce_bool(context.get("heiglogo_color"))
        vintage = resolve_vintage(context.get("heiglogo_year"), context.get("date"))
        left = _coerce_length(context.get("heiglogo_left"), name="left")
        top = _coerce_length(context.get("heiglogo_top"), name="top")
        return HeigLogoConfig(color=color, year=vintage, left=left, top=top)

    def inject(
        self,
        config: HeigLogoConfig,
        context: dict[str, Any],
        overrides: Mapping[str, Any] | None = None,
        *,
        emitter: DiagnosticEmitter | None = None,
    ) -> None:
        _ = overrides
        _ = emitter
        context["heiglogo_color"] = config.color
        context["heiglogo_year"] = config.year
        context["heiglogo_left"] = config.left
        context["heiglogo_top"] = config.top

    def should_render(self, config: HeigLogoConfig) -> bool:
        _ = config
        return True
