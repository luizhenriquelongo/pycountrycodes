from typing import (
    List,
    Optional,
)

from pydantic import BaseModel


def get_object_using_binary_search(array: List[BaseModel], field: str, value: str) -> Optional[BaseModel]:
    """
    It takes an array of objects, a field name, and a value, and returns the first object in the array that has a field with
    the given name and value

    Args:
      array (List[BaseModel]): The array to search through.
      field (str): The field to search on.
      value (str): The value to search for.

    Returns:
      The object that matches the value.
    """
    filtered_array = list(filter(lambda obj: getattr(obj, field, None) is not None, array))
    filtered_array.sort(key=lambda obj: getattr(obj, field, None))

    value = value.lower()

    low = 0
    high = len(filtered_array) - 1

    while low <= high:
        mid = (high + low) // 2

        if getattr(filtered_array[mid], field).lower() < value:
            low = mid + 1

        elif getattr(filtered_array[mid], field).lower() > value:
            high = mid - 1

        else:
            return filtered_array[mid]

    return None
