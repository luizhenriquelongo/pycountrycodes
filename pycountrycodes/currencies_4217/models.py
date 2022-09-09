from typing import (
    Any,
    List,
    Optional,
    Union,
)

from pycountrycodes.core.models import (
    BaseDataClass,
    Database,
)


class Currency(BaseDataClass):
    alpha_3: str
    name: str
    numeric: str

    @staticmethod
    def get_searchable_fields() -> List[str]:
        return ["name"]


class Currencies(Database):
    dataclass = Currency

    def get(self, **kwargs) -> Optional[Union[List[Currency], Currency]]:
        """
        This function returns a currency object from the database or a list of currency objects, if it exists.

        Returns:
          A Currency object or a List of Currencies

        Examples:
            Get a currency by its alpha_3:

            >>> currency = currencies.get(alpha_3='USD')
            >>> print(currency.name)
            'US Dollar'
        """
        multiple_results_lookup_fields = ["name"]
        return super(Currencies, self).get(multiple_results_lookup_fields=multiple_results_lookup_fields, **kwargs)

    def lookup(self, value: str, default: Any = None, **kwargs) -> Optional[Currency]:
        """
        It looks for a currency where the alpha_3 code is equal to a given value,
        and returns the first object that matches

        Args:
          value (str): The value to search for
          default (Any): The default value to return if no object is found

        Returns:
          The object of type Currency if found else None

        Examples:
            Lookup for a Currency with the alpha_3 'USD':

            >>> currency = currencies.lookup('USD')
            >>> print(currency.name)
            'US Dollar'
        """
        fields_to_lookup = ["alpha_3"]
        return super(Currencies, self).lookup(value, fields_to_lookup, default)
