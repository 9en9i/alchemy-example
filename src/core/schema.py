from collections.abc import Sequence
from typing import Any, Self, cast, overload

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Schema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    @classmethod
    @overload
    def cast(cls, data: Sequence[object]) -> list[Self]: ...

    @classmethod
    @overload
    def cast(cls, data: None) -> None: ...

    @classmethod
    @overload
    def cast(cls, data: object) -> Self: ...

    @classmethod
    def cast(cls, data: Any) -> Any:
        return cast(cls, data)
