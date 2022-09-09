import pytest
import pytest_mock

from pycountrycodes.core.models import ISOCodes
from pycountrycodes.currencies_4217 import models


@pytest.fixture(scope="module")
def currencies():
    return models.Currencies(ISOCodes.i4217)


class TestCurrenciesClass:
    def test_get_method_should_return_multiple_results_for_name(self, currencies):
        options = currencies.get(name="Leone")
        assert isinstance(options, list)
        assert options == [
            models.Currency(name="Leone", alpha_3="SLE", numeric="925"),
            models.Currency(name="Leone", alpha_3="SLL", numeric="694"),
        ]

    def test_get_method_should_return_only_one_result_for_alpha_3(self, currencies):
        currency = currencies.get(alpha_3="USD")
        assert currency is not None
        assert isinstance(currency, models.Currency)

    def test_get_method_should_not_accept_multiple_criteria(self, currencies):
        with pytest.raises(TypeError):
            currencies.get(name="US Dollar", alpha_3="USD")

    def test_get_method_should_not_accept_attributes_not_present_in_model(self, currencies):
        with pytest.raises(AttributeError):
            currencies.get(random_attribute="Bitcoin")

    def test_get_method_argument_type_should_be_string_always(self, currencies):
        with pytest.raises(TypeError):
            currencies.get(name=123)

    def test_get_method_returns_default_argument_when_country_not_found(self, currencies):
        default = "Some random default string"
        currency = currencies.get(name="", default=default)
        assert currency == default

    def test_search_method_returns_the_right_list_for_default_match_score(self, currencies):
        results = currencies.search("Real")
        assert isinstance(results, list)
        assert results == [
            models.Currency(alpha_3="KHR", name="Riel", numeric="116"),
            models.Currency(alpha_3="BRL", name="Brazilian Real", numeric="986"),
            models.Currency(alpha_3="COU", name="Unidad de Valor Real", numeric="970"),
            models.Currency(alpha_3="GTQ", name="Quetzal", numeric="320"),
            models.Currency(alpha_3="OMR", name="Rial Omani", numeric="512"),
            models.Currency(alpha_3="ZAR", name="Rand", numeric="710"),
            models.Currency(alpha_3="QAR", name="Qatari Rial", numeric="634"),
            models.Currency(alpha_3="YER", name="Yemeni Rial", numeric="886"),
            models.Currency(alpha_3="IRR", name="Iranian Rial", numeric="364"),
            models.Currency(alpha_3="NGN", name="Naira", numeric="566"),
            models.Currency(alpha_3="STN", name="Dobra", numeric="930"),
            models.Currency(alpha_3="XSU", name="Sucre", numeric="994"),
            models.Currency(alpha_3="NPR", name="Nepalese Rupee", numeric="524"),
            models.Currency(alpha_3="WST", name="Tala", numeric="882"),
            models.Currency(alpha_3="SAR", name="Saudi Riyal", numeric="682"),
            models.Currency(alpha_3="GIP", name="Gibraltar Pound", numeric="292"),
            models.Currency(alpha_3="KPW", name="North Korean Won", numeric="408"),
            models.Currency(alpha_3="AUD", name="Australian Dollar", numeric="036"),
            models.Currency(alpha_3="HNL", name="Lempira", numeric="340"),
            models.Currency(alpha_3="UYW", name="Unidad Previsional", numeric="927"),
            models.Currency(alpha_3="ILS", name="New Israeli Sheqel", numeric="376"),
            models.Currency(alpha_3="NZD", name="New Zealand Dollar", numeric="554"),
        ]

    def test_search_method_returns_options_over_score_cutoff(self, currencies):
        match_score_cutoff = 75
        results = currencies.search("Real", match_score_cutoff=match_score_cutoff)
        assert isinstance(results, list)
        assert results == [models.Currency(alpha_3="KHR", name="Riel", numeric="116")]
        assert results[0].match_score >= match_score_cutoff

    def test_search_method_raises_when_no_searchable_fields(self, currencies, mocker: pytest_mock.MockerFixture):
        mocked_dataclass = mocker.patch("pycountrycodes.Currencies.dataclass", mocker.Mock())
        mocked_dataclass.get_searchable_fields = mocker.Mock()
        mocked_dataclass.get_searchable_fields.return_value = []

        with pytest.raises(AttributeError):
            currencies.search("Dollar")

        mocked_dataclass.get_searchable_fields.assert_called_once()

    def test_lookup_method_using_alpha_3(self, currencies):
        result = currencies.lookup("USD")
        assert isinstance(result, models.Currency)
        assert result == models.Currency(alpha_3="USD", name="US Dollar", numeric="840")

    def test_lookup_method_should_return_none_for_not_found_subdivision(self, currencies):
        result = currencies.lookup("ZZZ")
        assert result is None
