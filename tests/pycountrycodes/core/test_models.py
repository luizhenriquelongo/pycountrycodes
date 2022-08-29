from pycountrycodes import (
    countries,
    subdivisions,
)
from pycountrycodes.core import models
from pycountrycodes.countries_3166_1.models import Country
from pycountrycodes.subdivisions_3166_2.models import Subdivision


class TestISOCodesEnum:
    def test_is_able_to_check_when_enum_contains_a_value(self):
        assert "3166-1" in models.ISOCodes
        assert "3166-2" in models.ISOCodes

    def test_is_able_to_check_when_enum_does_not_contains_a_value(self):
        assert "3166-3" not in models.ISOCodes


class TestDatabase:
    def test_if_is_able_iter_over_database_object_directly(self):
        for country in countries:
            assert isinstance(country, Country)

        for subdivision in subdivisions:
            assert isinstance(subdivision, Subdivision)

    def test_len_method(self):
        assert len(countries) == 249
        assert len(subdivisions) == 5123
