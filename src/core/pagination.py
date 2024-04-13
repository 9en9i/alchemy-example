from fastapi import Query
from pydantic import BaseModel as PydanticBaseModel


class LimitOffsetPagination(PydanticBaseModel):
    offset: int = Query(default=0, ge=0)
    limit: int = Query(default=100, ge=1)
