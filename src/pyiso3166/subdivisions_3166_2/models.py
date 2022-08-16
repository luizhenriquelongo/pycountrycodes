from typing import (
    List,
    Optional,
    Union,
)

from core import models
from countries.models import Country


class Subdivision(models.BaseDataClass):
    name: str
    code: str
    type: str
    country_code: str
    parent_code: Optional[str]

    @property
    def country(self) -> Optional[Country]:
        from src.pyiso3166 import countries

        return countries.get(alpha_2=self.country_code)

    @property
    def parent(self) -> Optional["Subdivision"]:
        if self.parent_code is None:
            return None
        from src.pyiso3166 import subdivisions

        return subdivisions.get(code=self.parent_code)

    @staticmethod
    def get_searchable_fields() -> List[str]:
        return ["name"]


class Subdivisions(models.Database):
    dataclass = Subdivision

    def get(self, **kwargs) -> Optional[Union[List[Subdivision], Subdivision]]:
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
