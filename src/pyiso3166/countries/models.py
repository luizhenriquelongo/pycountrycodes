from typing import (
    List,
    Optional,
)

from pydantic import (
    BaseModel,
    Extra,
)

from core.models import (
    Database,
)


class Country(BaseModel):
    name: str
    alpha_2: str
    alpha_3: str
    flag: str
    numeric: str
    official_name: Optional[str]
    common_name: Optional[str]

    class Config:
        extra = Extra.forbid


class Countries(Database):
    database: List[Country]
    dataclass = Country
