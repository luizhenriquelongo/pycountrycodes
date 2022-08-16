import pytest
import pytest_mock

from core.models import ISOCodes
from countries_3166_1 import models as countries_models
from subdivisions_3166_2 import models


@pytest.fixture(scope="module")
def subdivisions():
    return models.Subdivisions(ISOCodes.i3166_2)


class TestSubdivisionsClass:
    def test_get_method_should_return_multiple_results_for_name(self, subdivisions):
        options = subdivisions.get(name="Birmingham")
        assert isinstance(options, list)
        assert options == [
            models.Subdivision(
                name="Birmingham", code="GB-BIR", type="Metropolitan district", country_code="GB", parent_code=None
            )
        ]

    def test_get_method_should_return_multiple_results_for_type(self, subdivisions):
        options = subdivisions.get(type="Metropolitan district")
        assert isinstance(options, list)
        assert len(options) >= 1

    def test_get_method_should_return_multiple_results_for_country_code(self, subdivisions):
        options = subdivisions.get(country_code="gb")
        assert isinstance(options, list)
        assert len(options) >= 1

    def test_get_method_should_return_only_one_result_for_code(self, subdivisions):
        subdivision = subdivisions.get(code="GB-BIR")
        assert subdivision is not None
        assert isinstance(subdivision, models.Subdivision)

    def test_get_method_should_not_accept_multiple_criteria(self, subdivisions):
        with pytest.raises(TypeError):
            subdivisions.get(name="Birmingham", code="GB-BIR")

    def test_get_method_should_not_accept_attributes_not_present_in_model(self, subdivisions):
        with pytest.raises(AttributeError):
            subdivisions.get(random_attribute="Birmingham")

    def test_get_method_argument_type_should_be_string_always(self, subdivisions):
        with pytest.raises(TypeError):
            subdivisions.get(name=123)

    def test_get_method_returns_default_argument_when_country_not_found(self, subdivisions):
        default = "Some random default string"
        country = subdivisions.get(name="", default=default)
        assert country == default

    def test_search_method_returns_the_right_list_for_default_match_score(self, subdivisions):
        results = subdivisions.search("New Brunswick")
        assert isinstance(results, list)
        assert results == [
            models.Subdivision(
                name="New Brunswick", code="CA-NB", type="Province", country_code="CA", parent_code=None
            ),
            models.Subdivision(name="New York", code="US-NY", type="State", country_code="US", parent_code=None),
            models.Subdivision(name="New Jersey", code="US-NJ", type="State", country_code="US", parent_code=None),
            models.Subdivision(name="Nebraska", code="US-NE", type="State", country_code="US", parent_code=None),
            models.Subdivision(name="New Ireland", code="PG-NIK", type="Province", country_code="PG", parent_code=None),
            models.Subdivision(name="Wicklow", code="IE-WW", type="County", country_code="IE", parent_code="IE-L"),
            models.Subdivision(name="Ruse", code="BG-18", type="District", country_code="BG", parent_code=None),
            models.Subdivision(name="Bern", code="CH-BE", type="Canton", country_code="CH", parent_code=None),
            models.Subdivision(name="Brindisi", code="IT-BR", type="Province", country_code="IT", parent_code="IT-75"),
            models.Subdivision(
                name="Brvenica", code="MK-602", type="Municipality", country_code="MK", parent_code=None
            ),
            models.Subdivision(name="New Mexico", code="US-NM", type="State", country_code="US", parent_code=None),
            models.Subdivision(name="Beroun", code="CZ-202", type="District", country_code="CZ", parent_code="CZ-20"),
            models.Subdivision(name="El Beni", code="BO-B", type="Department", country_code="BO", parent_code=None),
            models.Subdivision(
                name="East New Britain", code="PG-EBR", type="Province", country_code="PG", parent_code=None
            ),
            models.Subdivision(
                name="West New Britain", code="PG-WBK", type="Province", country_code="PG", parent_code=None
            ),
            models.Subdivision(name="New Providence", code="BS-NP", type="Island", country_code="BS", parent_code=None),
            models.Subdivision(name="Busia", code="KE-04", type="County", country_code="KE", parent_code=None),
            models.Subdivision(name="Busia", code="UG-202", type="District", country_code="UG", parent_code="UG-E"),
            models.Subdivision(name="Nebbi", code="UG-310", type="District", country_code="UG", parent_code="UG-N"),
            models.Subdivision(
                name="Greenwich", code="GB-GRE", type="London borough", country_code="GB", parent_code=None
            ),
            models.Subdivision(name="Pernik", code="BG-14", type="District", country_code="BG", parent_code=None),
            models.Subdivision(name="Limerick", code="IE-LK", type="County", country_code="IE", parent_code="IE-M"),
            models.Subdivision(name="Wanica", code="SR-WA", type="District", country_code="SR", parent_code=None),
            models.Subdivision(name="Neno", code="MW-NE", type="District", country_code="MW", parent_code="MW-S"),
            models.Subdivision(name="Nyeri", code="KE-36", type="County", country_code="KE", parent_code=None),
            models.Subdivision(
                name="Borovnica", code="SI-005", type="Municipality", country_code="SI", parent_code=None
            ),
            models.Subdivision(
                name="Dobrovnik", code="SI-156", type="Municipality", country_code="SI", parent_code=None
            ),
            models.Subdivision(name="Ben Arous", code="TN-13", type="Governorate", country_code="TN", parent_code=None),
            models.Subdivision(
                name="New Taipei", code="TW-NWT", type="Special municipality", country_code="TW", parent_code=None
            ),
            models.Subdivision(
                name="Monte Cristi", code="DO-15", type="Province", country_code="DO", parent_code="DO-34"
            ),
            models.Subdivision(
                name="Warwickshire", code="GB-WAR", type="Two-tier county", country_code="GB", parent_code=None
            ),
            models.Subdivision(name="Bilecik", code="TR-11", type="Province", country_code="TR", parent_code=None),
        ]

    def test_search_method_returns_options_over_score_cutoff(self, subdivisions):
        match_score_cutoff = 75
        results = subdivisions.search("New Brunswick", match_score_cutoff=match_score_cutoff)
        assert isinstance(results, list)
        assert results == [
            models.Subdivision(name="New Brunswick", code="CA-NB", type="Province", country_code="CA", parent_code=None)
        ]
        assert results[0].match_score >= match_score_cutoff

    def test_search_method_raises_when_no_searchable_fields(self, subdivisions, mocker: pytest_mock.MockerFixture):
        mocked_dataclass = mocker.patch("src.pyiso3166.Subdivisions.dataclass", mocker.Mock())
        mocked_dataclass.get_searchable_fields = mocker.Mock()
        mocked_dataclass.get_searchable_fields.return_value = []

        with pytest.raises(AttributeError):
            subdivisions.search("New Brunswick")

        mocked_dataclass.get_searchable_fields.assert_called_once()


class TestSubdivisionClass:
    def test_if_model_can_get_country(self, subdivisions):
        subdivision = subdivisions.get(code="GB-BIR")
        assert isinstance(subdivision.country, countries_models.Country)

    def test_if_model_can_get_parent(self, subdivisions):
        subdivision = subdivisions.get(code="FR-63")
        assert isinstance(subdivision.parent, models.Subdivision)
        assert subdivision.parent == models.Subdivision(
            name="Auvergne-Rhône-Alpes", code="FR-ARA", type="Metropolitan region", country_code="FR", parent_code=None
        )
        assert subdivision.parent.parent is None
