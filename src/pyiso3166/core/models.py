import abc
import json
from enum import (
    Enum,
    EnumMeta,
)
from typing import (
    List,
    Type,
)

from pydantic import (
    BaseModel,
)

from core.binary_search import get_index_using_binary_search
from core.config import BASE_DIR
from core.exceptions import GetByAttributeNotAvailableError


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


class DatabaseDataclass(abc.ABC, BaseModel):
    @classmethod
    def fields_to_ignore(cls) -> List[str]:
        """ Ignore all non required fields to avoid error while sorting"""
        return [
            field for field, value in cls.__fields__.items()
            if value.required is False
        ]


class Database(abc.ABC):
    database: List['dataclass']

    def __init__(self, isocode: ISOCodes):
        self.__isocode = isocode
        self.database = self._populate_database()

    def __iter__(self):
        return iter(self.database)

    def __len__(self):
        return len(self.database)

    def get(self, **kwargs):
        kwargs.setdefault("default", None)
        default = kwargs.pop("default")

        if len(kwargs) != 1:
            raise TypeError("Only one criteria may be given")

        field, value = kwargs.popitem()
        if field not in self.dataclass.__fields__:
            raise AttributeError(f'{self.dataclass.__str__} model has no attribute {field}.')

        if field in self.dataclass.fields_to_ignore():
            raise GetByAttributeNotAvailableError(f'get by "{field}" is not available.')

        if not isinstance(value, str):
            raise TypeError(f'The value "{value}" must be a string.')

        value = value.strip()
        index = get_index_using_binary_search(self.database, field, value)
        if index is None:
            return default
        return self.database[index]

    def _populate_database(self) -> List['dataclass']:
        data = self._load_data_from_file()
        return [self.dataclass(**item) for item in data]

    def _load_data_from_file(self) -> List:
        with open(BASE_DIR / "iso" / f"{self.__isocode}.json", mode="r") as file:
            data = json.load(file)

        return data[self.__isocode]

    @property
    @abc.abstractmethod
    def dataclass(self) -> Type[DatabaseDataclass]:
        ...
