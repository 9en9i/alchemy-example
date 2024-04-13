from collections.abc import AsyncGenerator
from typing import Annotated, TypeAlias, TypeVar

from fastapi import Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.session import local_session

_T = TypeVar("_T")

Inject: TypeAlias = Annotated[_T, Depends()]
type InjectFromPath[T] = Annotated[T, Path(...)]
type InjectFromQuery[T] = Annotated[T, Query()]


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as db:
        try:
            yield db
        finally:
            await db.close()


InjectSession: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
