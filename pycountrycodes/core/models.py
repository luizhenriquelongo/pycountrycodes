import abc
import copy
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

from pydantic import (
    BaseModel,
    Extra,
    PrivateAttr,
)
from rapidfuzz import fuzz

from pycountrycodes.core import utils
from pycountrycodes.core.binary_search import get_object_using_binary_search
from pycountrycodes.core.config import BASE_DIR


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
    i4217 = "4217"


class BaseDataClass(abc.ABC, BaseModel):
    _match_score: Optional[float] = PrivateAttr(None)

    @property
    def match_score(self) -> float:
        return self._match_score

    @staticmethod
    @abc.abstractmethod
    def get_searchable_fields() -> List[str]:
        ...

    def update_match_score(self, match_score: Optional[float]):
        if match_score is None:
            return

        self._match_score = match_score

    class Config:
        extra = Extra.forbid


class Database(abc.ABC):
    database: List["dataclass"]

    def __init__(self, isocode: ISOCodes):
        self.__isocode = isocode
        self.database = self._populate_database()

    def __iter__(self):
        return iter(self.database)

    def __len__(self):
        return len(self.database)

    @abc.abstractmethod
    def get(
        self, *, multiple_results_lookup_fields: Optional[List[str]] = None, **kwargs
    ) -> Optional[Union[BaseDataClass, List[BaseDataClass]]]:
        """
        > If the field is in the list of fields that can have multiple results, return a list of all objects that match
        the value. Otherwise, return the first object that matches the value

        Args:
          multiple_results_lookup_fields (Optional[List[str]]): This is a list of fields that can have multiple results.
        For example, if you have a list of people, and you want to search for people with the same last name, you would
        pass in ["last_name"] as the value for this parameter.

        Returns:
          The object that matches the field and value, or the default if no match is found.
        """
        if multiple_results_lookup_fields is None:
            multiple_results_lookup_fields = []

        field, value, default = self._get_field_value_and_default_from_kwargs(kwargs)
        if field in multiple_results_lookup_fields:
            options = list(filter(lambda obj: getattr(obj, field, "").strip().lower() == value.lower(), self.database))
            return options if options else default

        else:
            obj = get_object_using_binary_search(self.database, field, value)
            return obj if obj is not None else default

    def search(self, query: str, *, match_score_cutoff: float = 50) -> List[BaseDataClass]:
        """
        It takes a query string, and returns a list of objects that match the query

        Args:
          query (str): The query string to search for.
          match_score_cutoff (float): The minimum score a match must have to be returned. Defaults to 50

        Returns:
          A list of specified dataclass objects.
        """
        searchable_fields = self.dataclass.get_searchable_fields()
        if not searchable_fields:
            raise AttributeError(f"Method not available for class {self.dataclass.__name__}")

        query = utils.remove_accents(query.strip().lower())
        options = self.get_options(query, searchable_fields, match_score_cutoff)
        return options

    def get_options(self, query: str, searchable_fields: List[str], score_cutoff: float) -> List[BaseDataClass]:
        """
        It takes a query string, a list of fields that are searchable, and a score cutoff, and returns a list of objects
        that match the query string in the specified fields with a score greater than or equal to the score cutoff

        Args:
          query (str): The string that you want to search for.
          searchable_fields (List[str]): A list of strings that are the names of the fields that search is available.
          score_cutoff (float): The minimum score that an option must have to be returned.

        Returns:
          A list of the specified dataclass objects.
        """
        options = copy.copy(self.database)
        for item in options:
            total_score = 0
            fields_used = 0
            for field in searchable_fields:
                field_value = getattr(item, field, None)
                if field_value is not None:
                    ratio_score = fuzz.ratio(query, utils.remove_accents(field_value.strip().lower()))
                    partial_score = fuzz.partial_ratio(query, field_value.strip().lower())
                    average_score = (ratio_score + partial_score) / 2

                    total_score += average_score
                    fields_used += 1

                else:
                    continue

            try:
                match_score = total_score / fields_used
                item.update_match_score(match_score=match_score)
            except ZeroDivisionError:
                item.update_match_score(match_score=0)

        options.sort(key=lambda obj: obj.match_score, reverse=True)
        return list(filter(lambda obj: obj.match_score >= score_cutoff, options))

    @abc.abstractmethod
    def lookup(self, value: str, fields_to_lookup: List[str], default: Any = None) -> Optional[BaseDataClass]:
        """
        It looks for a value in a list of fields, and returns the first object that matches

        Args:
          value (str): The value to search for
          fields_to_lookup (List[str]): List of fields to lookup
          default (Any): The default value to return if no object is found

        Returns:
          The object of type BaseDataClass if found else None
        """
        searchable_fields = self.dataclass.get_searchable_fields()
        if not searchable_fields:
            raise AttributeError(f"Method not available for class {self.dataclass.__name__}")

        value = utils.remove_accents(value.strip().lower())

        obj = None
        for field in fields_to_lookup:
            obj = get_object_using_binary_search(self.database, field, value)
            if obj is not None:
                break

        return obj if obj is not None else default

    def _populate_database(self) -> List[BaseDataClass]:
        """
        > It loads data from a file, and then creates a list of objects from that data

        Returns:
          A list of specified dataclass objects
        """
        data = self._load_data_from_file()
        return [self.dataclass(**item) for item in data]

    def _load_data_from_file(self) -> List:
        """
        It opens a file, reads the data, and returns the data

        Returns:
          A list of dictionaries.
        """
        with open(BASE_DIR / "iso" / f"{self.__isocode}.json", mode="r") as file:
            data = json.load(file)

        return data[self.__isocode]

    def _validate_field(self, field: str):
        """
        If the field is not in the dataclass, raise an AttributeError

        Args:
          field (str): The name of the field to get.
        """
        if field not in self.dataclass.__fields__:
            raise AttributeError(
                f'{self.dataclass.__name__} allows get() only for {", ".join(self.dataclass.__fields__)}.'
            )

    def _validate_value(self, value: str):
        """
        If the value is not a string, raise a TypeError.

        Args:
          value (str): The value to validate.
        """
        if not isinstance(value, str):
            raise TypeError(f'The value "{value}" must be a string.')

    def _get_field_value_and_default_from_kwargs(self, kwargs: dict) -> Tuple[str, str, Optional[Any]]:
        """
        It takes a dictionary of keyword arguments, and returns a tuple of three values: the field name,
        the field value, and the default value.

        Args:
          kwargs (dict): The keyword arguments passed to the function.

        Returns:
          A tuple of the field, value, and default.
        """
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
    def dataclass(self) -> Type[BaseDataClass]:
        ...
