from typing import (
    Any,
    List,
    Optional,
    Union,
)

from pycountrycodes.core import models
from pycountrycodes.countries_3166_1.models import Country


class Subdivision(models.BaseDataClass):
    name: str
    code: str
    type: str
    country_code: str
    parent_code: Optional[str]

    @property
    def country(self) -> Optional[Country]:
        from pycountrycodes import countries

        return countries.get(alpha_2=self.country_code)

    @property
    def parent(self) -> Optional["Subdivision"]:
        if self.parent_code is None:
            return None
        from pycountrycodes import subdivisions

        return subdivisions.get(code=self.parent_code)

    @staticmethod
    def get_searchable_fields() -> List[str]:
        return ["name"]


class Subdivisions(models.Database):
    dataclass = Subdivision

    def get(self, **kwargs) -> Optional[Union[List[Subdivision], Subdivision]]:
        """
        This function returns a subdivision object from the database or a list of subdivision objects, if it exists.

        Returns:
          A Subdivision object or a List of Subdivisions

        Examples:
            Get a subdivision by its code:

            >>> subdivision = subdivisions.get(code='US-NY')
            >>> print(subdivision.name)
            'New York'

            Get all subdivision from a country:

            >>> all_subdivisions = subdivisions.get(country_code='US')
            >>> len(all_subdivisions)
            57
        """
        multiple_results_lookup_fields = ["name", "type", "country_code"]
        return super(Subdivisions, self).get(multiple_results_lookup_fields=multiple_results_lookup_fields, **kwargs)

    def _populate_database(self) -> List[Subdivision]:
        data = self._load_data_from_file()

        def _get_country_code(code: str) -> str:
            return code.split("-")[0]

        def _get_parent_code(parent: Optional[str], code: str) -> Optional[str]:
            if parent is None:
                return None

            return f"{_get_country_code(code)}-{parent}"

        return [
            self.dataclass(
                name=item["name"],
                code=item["code"],
                type=item["type"],
                country_code=_get_country_code(item["code"]),
                parent_code=_get_parent_code(parent=item.get("parent"), code=item["code"]),
            )
            for item in data
        ]

    def lookup(self, value: str, default: Any = None, **kwargs) -> Optional[Subdivision]:
        """
        It looks for a subdivision where the code is equal to a given value,
        and returns the first object that matches

        Args:
          value (str): The value to search for
          default (Any): The default value to return if no object is found

        Returns:
          The object of type Subdivision if found else None

        Examples:
            Lookup for a subdivision with the code 'US-NY':

            >>> subdivision = subdivisions.lookup('US-NY')
            >>> print(subdivision.name)
            'New York'
        """
        fields_to_lookup = ["code"]
        return super(Subdivisions, self).lookup(value, fields_to_lookup, default)
