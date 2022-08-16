from typing import (
    List,
    Optional,
)

from pyiso3166.core.models import (
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
