from typing import (
    List,
    Optional,
)

from pydantic import BaseModel


def get_object_using_binary_search(array: List[BaseModel], field: str, value: str) -> Optional[BaseModel]:
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
