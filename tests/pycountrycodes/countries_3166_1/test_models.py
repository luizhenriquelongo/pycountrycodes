import pytest
import pytest_mock

from pycountrycodes.core.models import ISOCodes
from pycountrycodes.countries_3166_1 import models
from pycountrycodes.countries_3166_1.models import Country


class TestCountriesClass:
    countries = models.Countries(ISOCodes.i3166_1)

    def test_get_method_should_work_for_all_fields(self):
        assert self.countries.get(name="United Kingdom") == models.Country(
            name="United Kingdom",
            alpha_2="GB",
            alpha_3="GBR",
            flag="🇬🇧",
            numeric="826",
            official_name="United Kingdom of Great Britain and Northern Ireland",
            common_name=None,
        )
        assert self.countries.get(alpha_2="GB") == models.Country(
            name="United Kingdom",
            alpha_2="GB",
            alpha_3="GBR",
            flag="🇬🇧",
            numeric="826",
            official_name="United Kingdom of Great Britain and Northern Ireland",
            common_name=None,
        )
        assert self.countries.get(alpha_3="GBR") == models.Country(
            name="United Kingdom",
            alpha_2="GB",
            alpha_3="GBR",
            flag="🇬🇧",
            numeric="826",
            official_name="United Kingdom of Great Britain and Northern Ireland",
            common_name=None,
        )
        assert self.countries.get(official_name="Islamic Republic of Afghanistan") == models.Country(
            name="Afghanistan",
            alpha_2="AF",
            alpha_3="AFG",
            flag="🇦🇫",
            numeric="004",
            official_name="Islamic Republic of Afghanistan",
            common_name=None,
        )
        assert self.countries.get(common_name="Bolivia") == models.Country(
            name="Bolivia, Plurinational State of",
            alpha_2="BO",
            alpha_3="BOL",
            flag="🇧🇴",
            numeric="068",
            official_name="Plurinational State of Bolivia",
            common_name="Bolivia",
        )

    def test_get_method_should_not_accept_multiple_criteria(self):
        with pytest.raises(TypeError):
            self.countries.get(name="United Kingdom", alpha_2="GB")

    def test_get_method_should_not_accept_attributes_not_present_in_model(self):
        with pytest.raises(AttributeError):
            self.countries.get(random_attribute="United Kingdom")

    def test_get_method_argument_type_should_be_string_always(self):
        with pytest.raises(TypeError):
            self.countries.get(name=123)

    def test_get_method_returns_default_argument_when_country_not_found(self):
        default = "Some random default string"
        country = self.countries.get(name="", default=default)
        assert country == default

    def test_search_method_returns_the_right_list(self):
        results = self.countries.search("United")
        assert isinstance(results, list)
        assert results == [
            models.Country(
                name="United States",
                alpha_2="US",
                alpha_3="USA",
                flag="🇺🇸",
                numeric="840",
                official_name="United States of America",
                common_name=None,
            ),
            models.Country(
                name="United Arab Emirates",
                alpha_2="AE",
                alpha_3="ARE",
                flag="🇦🇪",
                numeric="784",
                official_name=None,
                common_name=None,
            ),
            models.Country(
                name="United Kingdom",
                alpha_2="GB",
                alpha_3="GBR",
                flag="🇬🇧",
                numeric="826",
                official_name="United Kingdom of Great Britain and Northern Ireland",
                common_name=None,
            ),
            models.Country(
                name="Niue",
                alpha_2="NU",
                alpha_3="NIU",
                flag="🇳🇺",
                numeric="570",
                official_name="Niue",
                common_name=None,
            ),
            models.Country(
                name="United States Minor Outlying Islands",
                alpha_2="UM",
                alpha_3="UMI",
                flag="🇺🇲",
                numeric="581",
                official_name=None,
                common_name=None,
            ),
            models.Country(
                name="Tanzania, United Republic of",
                alpha_2="TZ",
                alpha_3="TZA",
                flag="🇹🇿",
                numeric="834",
                official_name="United Republic of Tanzania",
                common_name="Tanzania",
            ),
            models.Country(
                name="Brunei Darussalam",
                alpha_2="BN",
                alpha_3="BRN",
                flag="🇧🇳",
                numeric="096",
                official_name=None,
                common_name=None,
            ),
            models.Country(
                name="Réunion",
                alpha_2="RE",
                alpha_3="REU",
                flag="🇷🇪",
                numeric="638",
                official_name=None,
                common_name=None,
            ),
        ]

    def test_search_method_returns_options_over_score_cutoff(self):
        match_score_cutoff = 75
        results = self.countries.search("United", match_score_cutoff=match_score_cutoff)
        assert isinstance(results, list)
        assert results == [
            models.Country(
                name="United States",
                alpha_2="US",
                alpha_3="USA",
                flag="🇺🇸",
                numeric="840",
                official_name="United States of America",
                common_name=None,
            )
        ]
        assert results[0].match_score >= match_score_cutoff

    def test_search_method_raises_when_no_searchable_fields(self, mocker: pytest_mock.MockerFixture):
        mocked_dataclass = mocker.patch("pycountrycodes.Countries.dataclass", mocker.Mock())
        mocked_dataclass.get_searchable_fields = mocker.Mock()
        mocked_dataclass.get_searchable_fields.return_value = []

        with pytest.raises(AttributeError):
            self.countries.search("United")

        mocked_dataclass.get_searchable_fields.assert_called_once()

    def test_lookup_method_using_name(self):
        result = self.countries.lookup("Brazil")
        assert isinstance(result, Country)
        assert result == models.Country(
            name="Brazil",
            alpha_2="BR",
            alpha_3="BRA",
            flag="🇧🇷",
            numeric="076",
            official_name="Federative Republic of Brazil",
            common_name=None,
        )

    def test_lookup_method_using_official_name(self):
        result = self.countries.lookup("Federative Republic of Brazil")
        assert isinstance(result, Country)
        assert result == models.Country(
            name="Brazil",
            alpha_2="BR",
            alpha_3="BRA",
            flag="🇧🇷",
            numeric="076",
            official_name="Federative Republic of Brazil",
            common_name=None,
        )

    def test_lookup_method_using_alpha_3(self):
        result = self.countries.lookup("BRA")
        assert isinstance(result, Country)
        assert result == models.Country(
            name="Brazil",
            alpha_2="BR",
            alpha_3="BRA",
            flag="🇧🇷",
            numeric="076",
            official_name="Federative Republic of Brazil",
            common_name=None,
        )

    def test_lookup_method_using_alpha_2(self):
        result = self.countries.lookup("BR")
        assert isinstance(result, Country)
        assert result == models.Country(
            name="Brazil",
            alpha_2="BR",
            alpha_3="BRA",
            flag="🇧🇷",
            numeric="076",
            official_name="Federative Republic of Brazil",
            common_name=None,
        )

    def test_lookup_method_should_return_none_for_not_found_country(self):
        result = self.countries.lookup("Brasil")
        assert result is None
