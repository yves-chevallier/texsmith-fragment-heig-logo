"""TeXSmith fragment exposing the HEIG-VD letterhead logo."""

from __future__ import annotations

from pathlib import Path

FRAGMENT_PATH: Path = Path(__file__).resolve().parent / "fragment"

__all__ = ["FRAGMENT_PATH"]
