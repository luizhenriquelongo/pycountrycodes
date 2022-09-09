from typing import (
    Any,
    List,
    Optional,
)

from pycountrycodes.core.models import (
    BaseDataClass,
    Database,
)


class Country(BaseDataClass):
    name: str
    alpha_2: str
    alpha_3: str
    flag: str
    numeric: str
    official_name: Optional[str]
    common_name: Optional[str]

    @staticmethod
    def get_searchable_fields() -> List[str]:
        return ["name", "official_name", "common_name"]


class Countries(Database):
    database: List[Country]
    dataclass = Country

    def get(self, **kwargs) -> Optional[Country]:
        """
        This function returns a country object from the database, if it exists

        Returns:
          A Country object

        Examples:
            Get a country by its name:

            >>> country = countries.get(name='United Kingdom')
            >>> print(country.alpha_2)
            'GB'
        """
        return super(Countries, self).get(**kwargs)

    def lookup(self, value: str, default: Any = None, **kwargs) -> Optional[Country]:
        """
        It looks for a countries where the name or official name are equal to a given value,
        and returns the first object that matches

        Args:
          value (str): The value to search for
          default (Any): The default value to return if no object is found

        Returns:
          The object of type Country if found else None

        Examples:
            Lookup for a country called 'Brazil':

            >>> country = countries.lookup('Brazil')
            >>> print(country.alpha_2)
            'BR'
        """
        fields_to_lookup = ["name", "official_name", "alpha_3", "alpha_2"]
        return super(Countries, self).lookup(value, fields_to_lookup, default)
