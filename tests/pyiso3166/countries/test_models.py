import pytest

from countries import models
from core.models import ISOCodes


class TestCountriesClass:
    countries = models.Countries(ISOCodes.i3166_1)

    def test_get_method_should_work_for_required_fields(self):
        assert self.countries.get(name='United Kingdom') == models.Country(
            name='United Kingdom',
            alpha_2='GB',
            alpha_3='GBR',
            flag='🇬🇧',
            numeric='826',
            official_name='United Kingdom of Great Britain and Northern Ireland',
            common_name=None
        )
        assert self.countries.get(alpha_2='GB') == models.Country(
            name='United Kingdom',
            alpha_2='GB',
            alpha_3='GBR',
            flag='🇬🇧',
            numeric='826',
            official_name='United Kingdom of Great Britain and Northern Ireland',
            common_name=None
        )
        assert self.countries.get(alpha_3='GBR') == models.Country(
            name='United Kingdom',
            alpha_2='GB',
            alpha_3='GBR',
            flag='🇬🇧',
            numeric='826',
            official_name='United Kingdom of Great Britain and Northern Ireland',
            common_name=None
        )
        assert self.countries.get(official_name='Islamic Republic of Afghanistan') == models.Country(
            name='Afghanistan',
            alpha_2='AF',
            alpha_3='AFG',
            flag='🇦🇫',
            numeric='004',
            official_name='Islamic Republic of Afghanistan',
            common_name=None
        )
        assert self.countries.get(common_name='Bolivia') == models.Country(
            name='Bolivia, Plurinational State of',
            alpha_2='BO',
            alpha_3='BOL',
            flag='🇧🇴',
            numeric='068',
            official_name='Plurinational State of Bolivia',
            common_name='Bolivia'
        )

    def test_get_method_should_not_accept_multiple_criteria(self):
        with pytest.raises(TypeError):
            self.countries.get(name='United Kingdom', alpha_2='GB')

    def test_get_method_should_not_accept_attributes_not_present_in_model(self):
        with pytest.raises(AttributeError):
            self.countries.get(random_attribute='United Kingdom')

    def test_get_method_argument_type_should_be_string_always(self):
        with pytest.raises(TypeError):
            self.countries.get(name=123)

    def test_get_method_returns_default_argument_when_country_not_found(self):
        default = 'Some random default string'
        country = self.countries.get(name='', default=default)
        assert country == default
