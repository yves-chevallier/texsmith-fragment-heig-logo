"""Integration tests for the OO HEIG-VD logo fragment."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import jinja2
import pytest

from texsmith_fragment_heig_logo import (
    FRAGMENT_PATH,
    HeigLogoConfig,
    HeigLogoFragment,
    fragment,
)


@pytest.fixture
def frag() -> HeigLogoFragment:
    return HeigLogoFragment()


def render_context(frag: HeigLogoFragment, context: dict) -> dict:
    """Run the fragment's build/inject pipeline and return the mutated context."""
    config = frag.render_context(context)
    assert isinstance(config, HeigLogoConfig)
    return context


class TestBuildConfig:
    def test_default_is_latest_vintage(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({})
        assert config.year == "2020"
        assert config.color is False

    def test_auto_year_from_iso_date(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({"heiglogo_year": "auto", "date": "2006-09-01"})
        assert config.year == "2004"

    def test_auto_year_from_localised_date(self, frag: HeigLogoFragment) -> None:
        # TeXSmith has already localised the date by the time fragments render.
        config = frag.build_config({"date": "5 mars 2011"})
        assert config.year == "2009"

    def test_auto_year_from_date_object(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({"date": date(1999, 1, 1)})
        assert config.year == "1998"

    def test_explicit_year_overrides_date(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({"heiglogo_year": "1998", "date": "2026-01-01"})
        assert config.year == "1998"

    def test_no_date_falls_back_to_latest(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({"date": ""})
        assert config.year == "2020"

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [(True, True), (False, False), ("true", True), ("no", False), (1, True)],
    )
    def test_color_coercion(self, frag: HeigLogoFragment, raw: object, expected: bool) -> None:
        config = frag.build_config({"heiglogo_color": raw})
        assert config.color is expected

    def test_unknown_year_raises(self, frag: HeigLogoFragment) -> None:
        with pytest.raises(ValueError, match="Unknown heiglogo year"):
            frag.build_config({"heiglogo_year": "1995"})


class TestInject:
    def test_inject_sets_context(self, frag: HeigLogoFragment) -> None:
        context: dict = {"heiglogo_year": "auto", "date": "2007-01-01"}
        render_context(frag, context)
        assert context["heiglogo_year"] == "2004"
        assert context["heiglogo_color"] is False

    def test_should_render_always_true(self, frag: HeigLogoFragment) -> None:
        assert frag.should_render(HeigLogoConfig(color=False, year="2020")) is True


class TestDeclaration:
    def test_name_and_pieces(self) -> None:
        assert fragment.name == "heiglogo"
        assert len(fragment.pieces) == 2
        kinds = {piece.kind for piece in fragment.pieces}
        assert kinds == {"package", "inline"}

    def test_piece_files_exist(self) -> None:
        for piece in fragment.pieces:
            assert piece.template_path.exists()

    def test_attribute_sources(self) -> None:
        assert fragment.attributes["heiglogo_year"].sources == [
            "heiglogo.year",
            "heiglogo_year",
        ]
        assert fragment.attributes["heiglogo_color"].sources == [
            "heiglogo.color",
            "heiglogo_color",
        ]

    def test_fragment_path_points_to_dir(self) -> None:
        assert FRAGMENT_PATH.is_dir()
        assert (FRAGMENT_PATH / "heiglogo.sty").is_file()


class TestTemplateRendering:
    """Render the inline Jinja piece with TeXSmith's LaTeX delimiters."""

    @staticmethod
    def _render(**context: object) -> str:
        env = jinja2.Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        source = (FRAGMENT_PATH / "heiglogo.jinja.tex").read_text()
        return env.from_string(source).render(**context)

    def test_year_is_emitted(self) -> None:
        out = self._render(heiglogo_year="2004", heiglogo_color=False)
        assert "year=2004" in out
        assert "color=true" not in out

    def test_color_block(self) -> None:
        out = self._render(heiglogo_year="2020", heiglogo_color=True)
        assert "year=2020" in out
        assert "color=true" in out

    def test_full_pipeline_then_render(self) -> None:
        context: dict = {"date": "2009-06-01", "heiglogo_color": "true"}
        fragment.render_context(context)
        out = self._render(**context)
        assert "year=2009" in out
        assert "color=true" in out


class TestRegistry:
    """The fragment should be discoverable through the entry point."""

    def test_registered_via_entry_point(self) -> None:
        from texsmith.core.fragments import FRAGMENT_REGISTRY

        resolved = FRAGMENT_REGISTRY.resolve("heiglogo")
        assert getattr(resolved, "name", None) == "heiglogo"
