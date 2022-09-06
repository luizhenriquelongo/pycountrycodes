from typing import (
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
