from typing import (
    List,
    Optional,
)

from pydantic import BaseModel


def get_index_using_binary_search(array: List[BaseModel], field: str, value: str) -> Optional[int]:
    array.sort(key=lambda obj: getattr(obj, field, None))

    value = value.lower()

    low = 0
    high = len(array) - 1

    while low <= high:
        mid = (high + low) // 2

        if getattr(array[mid], field).lower() < value:
            low = mid + 1

        elif getattr(array[mid], field).lower() > value:
            high = mid - 1

        else:
            return mid

    return None
