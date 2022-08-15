import abc
import json
from enum import (
    Enum,
    EnumMeta,
)
from typing import (
    Any,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)

from pydantic import BaseModel

from core.binary_search import get_object_using_binary_search
from core.config import BASE_DIR


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(str, Enum, metaclass=MetaEnum):
    ...


class ISOCodes(BaseEnum):
    i3166_1 = "3166-1"
    i3166_2 = "3166-2"


class Database(abc.ABC):
    database: List['dataclass']

    def __init__(self, isocode: ISOCodes):
        self.__isocode = isocode
        self.database = self._populate_database()

    def __iter__(self):
        return iter(self.database)

    def __len__(self):
        return len(self.database)

    def get(self, *, multiple_results_lookup_fields: Optional[List[str]] = None, **kwargs) -> Optional[Union[BaseModel, List[BaseModel]]]:
        if multiple_results_lookup_fields is None:
            multiple_results_lookup_fields = []

        field, value, default = self._get_field_value_and_default_from_kwargs(kwargs)
        if field in multiple_results_lookup_fields:
            options = list(filter(lambda obj: getattr(obj, field, '').strip().lower() == value.lower(), self.database))
            return options if options else default

        else:
            obj = get_object_using_binary_search(self.database, field, value)
            return obj if obj is not None else default

    def _populate_database(self) -> List['dataclass']:
        data = self._load_data_from_file()
        return [self.dataclass(**item) for item in data]

    def _load_data_from_file(self) -> List:
        with open(BASE_DIR / "iso" / f"{self.__isocode}.json", mode="r") as file:
            data = json.load(file)

        return data[self.__isocode]

    def _validate_field(self, field: str):
        if field not in self.dataclass.__fields__:
            raise AttributeError(
                f'{self.dataclass.__name__} allows get() only for {", ".join(self.dataclass.__fields__)}.'
            )

    def _validate_value(self, value: str):
        if not isinstance(value, str):
            raise TypeError(f'The value "{value}" must be a string.')

    def _get_field_value_and_default_from_kwargs(self, kwargs: dict) -> Tuple[str, str, Optional[Any]]:
        kwargs.setdefault("default", None)
        default = kwargs.pop("default")

        if len(kwargs) != 1:
            raise TypeError("Only one criteria may be given")

        field, value = kwargs.popitem()
        self._validate_field(field)
        self._validate_value(value)

        value = value.strip()
        return field, value, default

    @property
    @abc.abstractmethod
    def dataclass(self) -> Type[BaseModel]:
        ...
