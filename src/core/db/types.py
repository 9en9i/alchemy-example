from typing import Annotated, TypeAlias, TypeVar

from sqlalchemy.orm import mapped_column

_T = TypeVar("_T")

Primary: TypeAlias = Annotated[_T, mapped_column(primary_key=True)]
