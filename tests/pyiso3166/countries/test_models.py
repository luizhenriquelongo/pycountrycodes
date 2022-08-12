import pytest

from core.exceptions import GetByAttributeNotAvailableError
from countries import models
from core.models import ISOCodes


class TestCountryClass:
    def test_fields_to_ignore(self):
        assert models.Country.fields_to_ignore() == ['official_name', 'common_name']


class TestCountriesClass:
    countries = models.Countries(ISOCodes.i3166_1)

    def test_get_method_should_work_for_required_fields(self):
        assert self.countries.get(name='United Kingdom') is not None
        assert self.countries.get(alpha_2='GB') is not None
        assert self.countries.get(alpha_3='GBR') is not None

    def test_get_method_should_raise_for_non_required_fields(self):
        with pytest.raises(GetByAttributeNotAvailableError):
            self.countries.get(common_name='United Kingdom')

        with pytest.raises(GetByAttributeNotAvailableError):
            self.countries.get(official_name='United Kingdom')

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
