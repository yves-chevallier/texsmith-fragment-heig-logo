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

    def test_default_offsets(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({})
        assert (config.left, config.top) == ("1cm", "1cm")

    def test_explicit_offsets(self, frag: HeigLogoFragment) -> None:
        config = frag.build_config({"heiglogo_left": "17mm", "heiglogo_top": " 0.8cm "})
        assert (config.left, config.top) == ("17mm", "0.8cm")

    @pytest.mark.parametrize("raw", ["17", "mm", "1cm}", r"1cm\relax", "large"])
    def test_invalid_offset_raises(self, frag: HeigLogoFragment, raw: str) -> None:
        with pytest.raises(ValueError, match="Invalid heiglogo left"):
            frag.build_config({"heiglogo_left": raw})


class TestInject:
    def test_inject_sets_context(self, frag: HeigLogoFragment) -> None:
        context: dict = {"heiglogo_year": "auto", "date": "2007-01-01"}
        render_context(frag, context)
        assert context["heiglogo_year"] == "2004"
        assert context["heiglogo_color"] is False
        assert context["heiglogo_left"] == "1cm"
        assert context["heiglogo_top"] == "1cm"

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
        assert fragment.attributes["heiglogo_left"].sources == [
            "heiglogo.left",
            "heiglogo_left",
        ]
        assert fragment.attributes["heiglogo_top"].sources == [
            "heiglogo.top",
            "heiglogo_top",
        ]

    def test_fragment_path_points_to_dir(self) -> None:
        assert FRAGMENT_PATH.is_dir()
        assert (FRAGMENT_PATH / "heiglogo.sty").is_file()


class TestTemplateRendering:
    """Render the inline Jinja piece with TeXSmith's LaTeX delimiters."""

    @staticmethod
    def _render(**context: object) -> str:
        context = {"heiglogo_left": "1cm", "heiglogo_top": "1cm", **context}
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

    def test_offsets_are_emitted(self) -> None:
        out = self._render(
            heiglogo_year="2020", heiglogo_color=False, heiglogo_left="17mm"
        )
        assert "left=17mm,top=1cm" in out

    def test_full_pipeline_then_render(self) -> None:
        context: dict = {
            "date": "2009-06-01",
            "heiglogo_color": "true",
            "heiglogo_left": "17mm",
        }
        fragment.render_context(context)
        out = self._render(**context)
        assert "year=2009" in out
        assert "left=17mm" in out
        assert "color=true" in out


class TestApiSurface:
    """The bits of the 0.8 ``BaseFragment`` contract this fragment relies on."""

    def test_pieces_target_a_template_variable_not_a_slot(self) -> None:
        # 0.7 renamed ``FragmentPiece.slot`` to ``variable``; 0.8 raises when a
        # fragment targets a name the template declares as a document slot.
        for piece in fragment.pieces:
            assert piece.variable == "extra_packages"
            assert not hasattr(piece, "slot")

    def test_build_config_and_inject_accept_an_emitter(
        self, frag: HeigLogoFragment
    ) -> None:
        # ``render_fragments`` always passes ``emitter=`` by keyword.
        context: dict = {"date": "2011-01-01"}
        config = frag.build_config(context, overrides=None, emitter=None)
        assert config.year == "2009"
        frag.inject(config, context, overrides=None, emitter=None)
        assert context["heiglogo_year"] == "2009"

    def test_package_piece_output_filename(self) -> None:
        package = next(p for p in fragment.pieces if p.kind == "package")
        assert package.output_filename("heiglogo") == "heiglogo.sty"
        inline = next(p for p in fragment.pieces if p.kind == "inline")
        assert inline.output_filename("heiglogo") is None


class TestRegistry:
    """The fragment should be discoverable through the entry point."""

    def test_registered_via_entry_point(self) -> None:
        from texsmith.core.fragments import FRAGMENT_REGISTRY

        resolved = FRAGMENT_REGISTRY.resolve("heiglogo")
        assert getattr(resolved, "name", None) == "heiglogo"

    def test_manifest_resolves_to_the_same_object(self) -> None:
        # ``fragment.toml`` names the entrypoint, so resolving the directory by
        # path yields the very same singleton (and its auto-vintage logic).
        from texsmith.core.fragments import FRAGMENT_REGISTRY

        by_name = FRAGMENT_REGISTRY.resolve("heiglogo")
        by_path = FRAGMENT_REGISTRY.resolve(str(FRAGMENT_PATH))
        assert by_path is by_name

    def test_attributes_are_owned_by_the_fragment(self) -> None:
        from texsmith.core.fragments import FRAGMENT_REGISTRY

        FRAGMENT_REGISTRY.resolve("heiglogo")
        attributes = FRAGMENT_REGISTRY.attributes_for("heiglogo")
        assert set(attributes) == {
            "heiglogo_color",
            "heiglogo_year",
            "heiglogo_left",
            "heiglogo_top",
        }
        assert {spec.owner for spec in attributes.values()} == {"heiglogo"}

    def test_attribute_defaults_are_collected(self) -> None:
        from texsmith.core.fragments import collect_fragment_attribute_defaults

        defaults = collect_fragment_attribute_defaults(["heiglogo"])
        assert defaults == {
            "heiglogo_color": False,
            "heiglogo_year": "auto",
            "heiglogo_left": "1cm",
            "heiglogo_top": "1cm",
        }


class TestRenderFragments:
    """Drive TeXSmith's real rendering entry point end to end."""

    @staticmethod
    def _render(tmp_path: Path, **context: object) -> tuple[object, dict]:
        from texsmith.core.fragments import render_fragments

        payload: dict = dict(context)
        result = render_fragments(
            ["heiglogo"],
            context=payload,
            output_dir=tmp_path,
            declared_slots={"mainmatter", "abstract", "appendix", "backmatter"},
            declared_variables={"extra_packages"},
            template_name="article",
        )
        return result, payload

    def test_writes_the_package_and_injects_the_usepackage(self, tmp_path: Path) -> None:
        result, _ = self._render(tmp_path, date="2026-01-01")
        assert (tmp_path / "heiglogo.sty").is_file()
        assert result.packages == ["heiglogo"]
        injections = result.variable_injections["extra_packages"]
        assert injections[0] == "\\usepackage{heiglogo}"
        assert "year=2020" in injections[1]
        assert result.providers["extra_packages"] == ["heiglogo", "heiglogo"]

    def test_attribute_override_selects_the_vintage(self, tmp_path: Path) -> None:
        from texsmith.core.fragments import render_fragments

        payload: dict = {"date": "2026-01-01"}
        result = render_fragments(
            ["heiglogo"],
            context=payload,
            output_dir=tmp_path,
            overrides={"heiglogo": {"year": "1998", "color": True}},
            declared_variables={"extra_packages"},
            template_name="article",
        )
        inline = result.variable_injections["extra_packages"][1]
        assert "year=1998" in inline
        assert "color=true" in inline

    def test_attribute_override_moves_the_logo(self, tmp_path: Path) -> None:
        from texsmith.core.fragments import render_fragments

        result = render_fragments(
            ["heiglogo"],
            context={"date": "2026-01-01"},
            output_dir=tmp_path,
            overrides={"heiglogo": {"left": "17mm", "top": "12mm"}},
            declared_variables={"extra_packages"},
            template_name="article",
        )
        inline = result.variable_injections["extra_packages"][1]
        assert "left=17mm,top=12mm" in inline

    def test_auto_vintage_from_the_document_date(self, tmp_path: Path) -> None:
        _, payload = self._render(tmp_path, date="2006-09-01")
        assert payload["heiglogo_year"] == "2004"

    def test_targeting_a_declared_slot_is_refused(self, tmp_path: Path) -> None:
        from texsmith.core.fragments import render_fragments
        from texsmith.core.templates.manifest import TemplateError

        with pytest.raises(TemplateError, match="document slot"):
            render_fragments(
                ["heiglogo"],
                context={},
                output_dir=tmp_path,
                declared_slots={"extra_packages"},
                template_name="article",
            )
