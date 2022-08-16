from core import models
from countries_3166_1.models import Country
from src.pyiso3166 import (
    countries,
    subdivisions,
)
from subdivisions_3166_2.models import Subdivision


class TestEnum(models.BaseEnum):
    TEST1 = "test1"
    TEST2 = "test2"


class TestBaseEnum:
    def test_is_able_to_check_when_enum_contains_a_value(self):
        assert "test1" in TestEnum

    def test_is_able_to_check_when_enum_does_not_contains_a_value(self):
        assert "test3" not in TestEnum


class TestDatabase:
    def test_if_is_able_iter_over_database_object_directly(self):
        for country in countries:
            assert isinstance(country, Country)

        for subdivision in subdivisions:
            assert isinstance(subdivision, Subdivision)

    def test_len_method(self):
        assert len(countries) == 249
        assert len(subdivisions) == 5123
