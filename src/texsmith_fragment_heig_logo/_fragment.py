"""The object-oriented HEIG-VD logo fragment.

Kept separate from the package ``__init__`` so that importing the package does
not pull in TeXSmith at module load time. TeXSmith builds its fragment registry
*while* it is being imported and, as part of that, loads this package's entry
point; importing the heavy machinery eagerly here would create a circular
import. The entry point is the lazy factory :func:`.load_fragment`.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any, ClassVar

from texsmith.core.fragments.base import BaseFragment, FragmentPiece
from texsmith.core.templates.manifest import TemplateAttributeSpec

from ._vintage import LATEST_VINTAGE, VINTAGES, resolve_vintage

FRAGMENT_PATH: Path = Path(__file__).resolve().parent / "fragment"

__all__ = ["HeigLogoConfig", "HeigLogoFragment"]


def _coerce_bool(value: Any, *, default: bool = False) -> bool:
    """Interpret a front-matter value as a boolean, tolerating strings."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        token = value.strip().lower()
        if not token:
            return default
        if token in {"true", "yes", "on", "1"}:
            return True
        if token in {"false", "no", "off", "0"}:
            return False
    return default


class HeigLogoConfig:
    """Resolved fragment options handed to the Jinja template."""

    __slots__ = ("color", "year")

    def __init__(self, *, color: bool, year: str) -> None:
        self.color = color
        self.year = year

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"HeigLogoConfig(color={self.color!r}, year={self.year!r})"


class HeigLogoFragment(BaseFragment[HeigLogoConfig]):
    """HEIG-VD letterhead logo with selectable vintage."""

    name: ClassVar[str] = "heiglogo"
    description: ClassVar[str] = (
        "Logo HEIG-VD sur la première page, en haut à gauche, à 1cm des bords."
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
            slot="extra_packages",
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
    }
    config_cls: ClassVar[type[HeigLogoConfig]] = HeigLogoConfig
    source: ClassVar[Path] = FRAGMENT_PATH
    context_defaults: ClassVar[dict[str, Any]] = {
        "heiglogo_color": False,
        "heiglogo_year": LATEST_VINTAGE,
    }

    def build_config(
        self, context: Mapping[str, Any], overrides: Mapping[str, Any] | None = None
    ) -> HeigLogoConfig:
        _ = overrides
        color = _coerce_bool(context.get("heiglogo_color"))
        vintage = resolve_vintage(context.get("heiglogo_year"), context.get("date"))
        return HeigLogoConfig(color=color, year=vintage)

    def inject(
        self,
        config: HeigLogoConfig,
        context: dict[str, Any],
        overrides: Mapping[str, Any] | None = None,
    ) -> None:
        _ = overrides
        context["heiglogo_color"] = config.color
        context["heiglogo_year"] = config.year

    def should_render(self, config: HeigLogoConfig) -> bool:
        _ = config
        return True
