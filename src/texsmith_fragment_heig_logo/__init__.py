"""TeXSmith fragment exposing the HEIG-VD letterhead logo.

The fragment drops the HEIG-VD logo in the top-left corner of every page. It
supports the historical logo *vintages* shipped by the upstream package
(https://github.com/HEIG-VD/logos): ``1998``, ``2004``, ``2009`` and ``2020``.

The vintage is chosen either explicitly through the ``heiglogo.year`` front
matter attribute, or — by leaving it on its default ``"auto"`` — automatically
from the document ``date`` (see :mod:`._vintage`).

This module is intentionally lightweight: it does **not** import TeXSmith at
load time. TeXSmith builds its fragment registry while it is being imported and
loads this package's ``texsmith.fragments`` entry point as part of that, so an
eager import here would deadlock on a circular import. The entry point is the
lazy factory :func:`load_fragment`; ``fragment``/``HeigLogoFragment``/
``HeigLogoConfig`` are exposed through :pep:`562` lazy attribute access.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

FRAGMENT_PATH: Path = Path(__file__).resolve().parent / "fragment"

__all__ = ["FRAGMENT_PATH", "HeigLogoConfig", "HeigLogoFragment", "fragment", "load_fragment"]

_fragment_singleton: Any = None


def load_fragment() -> Any:
    """Return the singleton :class:`HeigLogoFragment` (the entry-point target).

    Importing TeXSmith's fragment machinery is deferred to here and ordered so
    that the registry is fully built before the fragment class is constructed,
    which keeps registration working even when this package is what first
    triggers the TeXSmith import.
    """
    global _fragment_singleton
    if _fragment_singleton is not None:
        return _fragment_singleton
    # Ensure the registry package finishes importing before we build the class,
    # so a re-entrant entry-point load (this package importing TeXSmith first)
    # still finds the class definition available.
    import texsmith.core.fragments  # noqa: F401

    from ._fragment import HeigLogoFragment

    if _fragment_singleton is None:
        _fragment_singleton = HeigLogoFragment()
    return _fragment_singleton


def __getattr__(name: str) -> Any:
    """Lazily expose the fragment symbols without importing TeXSmith eagerly."""
    if name == "fragment":
        return load_fragment()
    if name in {"HeigLogoFragment", "HeigLogoConfig"}:
        # Route through load_fragment first so TeXSmith's registry is fully
        # imported before ``_fragment`` is, avoiding a re-entrant circular load.
        load_fragment()
        from . import _fragment

        return getattr(_fragment, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:  # pragma: no cover - typing aid only
    from ._fragment import HeigLogoConfig, HeigLogoFragment

    fragment: HeigLogoFragment
