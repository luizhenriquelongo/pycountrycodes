import pytest

import countries.models
from countries import models as countries_models
from subdivisions import models
from core.models import ISOCodes


@pytest.fixture(scope='module')
def subdivisions():
    return models.Subdivisions(ISOCodes.i3166_2)


class TestSubdivisionsClass:
    def test_get_method_should_return_multiple_results_for_name(self, subdivisions):
        options = subdivisions.get(name='Birmingham')
        assert isinstance(options, list)
        assert options == [models.Subdivision(
            name='Birmingham',
            code='GB-BIR',
            type='Metropolitan district',
            country_code='GB',
            parent_code=None)
        ]

    def test_get_method_should_return_multiple_results_for_type(self, subdivisions):
        options = subdivisions.get(type='Metropolitan district')
        assert isinstance(options, list)
        assert len(options) >= 1

    def test_get_method_should_return_multiple_results_for_country_code(self, subdivisions):
        options = subdivisions.get(country_code='gb')
        assert isinstance(options, list)
        assert len(options) >= 1

    def test_get_method_should_return_only_one_result_for_code(self, subdivisions):
        subdivision = subdivisions.get(code='GB-BIR')
        assert subdivision is not None
        assert isinstance(subdivision, models.Subdivision)

    def test_get_method_should_not_accept_multiple_criteria(self, subdivisions):
        with pytest.raises(TypeError):
            subdivisions.get(name='Birmingham', code='GB-BIR')

    def test_get_method_should_not_accept_attributes_not_present_in_model(self, subdivisions):
        with pytest.raises(AttributeError):
            subdivisions.get(random_attribute='Birmingham')

    def test_get_method_argument_type_should_be_string_always(self, subdivisions):
        with pytest.raises(TypeError):
            subdivisions.get(name=123)

    def test_get_method_returns_default_argument_when_country_not_found(self, subdivisions):
        default = 'Some random default string'
        country = subdivisions.get(name='', default=default)
        assert country == default


class TestSubdivisionClass:
    def test_if_model_can_get_country(self, subdivisions):
        subdivision = subdivisions.get(code='GB-BIR')
        assert isinstance(subdivision.country, countries_models.Country)

    def test_if_model_can_get_parent(self, subdivisions):
        subdivision = subdivisions.get(code='FR-63')
        assert isinstance(subdivision.parent, models.Subdivision)
        assert subdivision.parent == models.Subdivision(
            name='Auvergne-Rhône-Alpes',
            code='FR-ARA',
            type='Metropolitan region',
            country_code='FR',
            parent_code=None
        )
        assert subdivision.parent.parent is None
