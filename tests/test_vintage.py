"""Unit tests for the pure vintage-selection logic."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from texsmith_fragment_heig_logo._vintage import (
    LATEST_VINTAGE,
    VINTAGES,
    extract_year,
    resolve_vintage,
    vintage_for_year,
)


class TestVintageForYear:
    @pytest.mark.parametrize(
        ("year", "expected"),
        [
            (1990, "1998"),  # before the oldest vintage -> oldest
            (1998, "1998"),
            (2003, "1998"),
            (2004, "2004"),  # introduction year is inclusive
            (2008, "2004"),
            (2009, "2009"),
            (2019, "2009"),
            (2020, "2020"),
            (2026, "2020"),
            (3000, "2020"),
        ],
    )
    def test_boundaries(self, year: int, expected: str) -> None:
        assert vintage_for_year(year) == expected

    def test_every_vintage_maps_to_itself(self) -> None:
        for vintage in VINTAGES:
            assert vintage_for_year(int(vintage)) == vintage


class TestExtractYear:
    def test_none(self) -> None:
        assert extract_year(None) is None

    def test_empty_string(self) -> None:
        assert extract_year("") is None
        assert extract_year("   ") is None

    def test_date_object(self) -> None:
        assert extract_year(date(2006, 5, 1)) == 2006

    def test_datetime_object(self) -> None:
        assert extract_year(datetime(2011, 1, 2, 3, 4)) == 2011

    def test_integer(self) -> None:
        assert extract_year(2015) == 2015

    def test_implausible_integer(self) -> None:
        assert extract_year(42) is None

    def test_bool_is_not_a_year(self) -> None:
        # bool is an int subclass; it must not be read as a year.
        assert extract_year(True) is None

    def test_iso_string(self) -> None:
        assert extract_year("2007-03-14") == 2007

    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("5 mars 2026", 2026),  # French long form (TeXSmith fr output)
            ("1er mars 2004", 2004),
            ("March 5, 2009", 2009),  # English long form
            ("Genève, le 2018", 2018),
        ],
    )
    def test_localised_long_form(self, text: str, expected: int) -> None:
        assert extract_year(text) == expected

    def test_no_year_returns_none(self) -> None:
        assert extract_year("sometime soon") is None

    def test_today_keyword(self) -> None:
        assert extract_year("today", today=date(2022, 7, 1)) == 2022
        assert extract_year("Today", today=date(2022, 7, 1)) == 2022


class TestResolveVintage:
    def test_default_when_nothing_known(self) -> None:
        assert resolve_vintage(None, None) == LATEST_VINTAGE

    def test_auto_keyword_defers_to_date(self) -> None:
        assert resolve_vintage("auto", "2006-01-01") == "2004"
        assert resolve_vintage("AUTO", date(2010, 1, 1)) == "2009"

    def test_empty_string_defers_to_date(self) -> None:
        assert resolve_vintage("", "1999-12-31") == "1998"

    def test_explicit_vintage_wins_over_date(self) -> None:
        assert resolve_vintage("1998", "2026-01-01") == "1998"
        assert resolve_vintage(2004, "2026-01-01") == "2004"

    def test_explicit_integer_vintage(self) -> None:
        assert resolve_vintage(2009, None) == "2009"

    def test_auto_without_date_uses_default(self) -> None:
        assert resolve_vintage("auto", None) == LATEST_VINTAGE
        assert resolve_vintage("auto", "no date here") == LATEST_VINTAGE

    def test_custom_default(self) -> None:
        assert resolve_vintage("auto", None, default="1998") == "1998"

    def test_unknown_vintage_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown heiglogo year"):
            resolve_vintage("2099", None)

    def test_today_keyword_flows_through(self) -> None:
        assert resolve_vintage("auto", "today", today=date(2003, 1, 1)) == "1998"
        assert resolve_vintage("auto", "today", today=date(2024, 1, 1)) == "2020"
