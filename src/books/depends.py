from typing import Annotated, TypeAlias, cast

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import joinedload, with_polymorphic
from sqlalchemy.orm.util import AliasedClass

from src.books.erros import PublicationNotFoundError
from src.core.depends import InjectFromPath, InjectSession
from src.database import (
    BookModel,
    MagazineModel,
    PublicationModel,
    UnionPublicationModel,
)


async def _get_publication_from_id_in_path(
    session: InjectSession,
    publication_id: InjectFromPath[int],
) -> PublicationModel:
    publication = await session.get(PublicationModel, publication_id)
    if publication is None:
        raise PublicationNotFoundError

    return publication


async def _get_union_publication_from_id_in_path(
    session: InjectSession,
    publication_id: InjectFromPath[int],
) -> UnionPublicationModel:
    polymorphic = cast(
        AliasedClass[UnionPublicationModel],
        with_polymorphic(PublicationModel, [BookModel, MagazineModel]),
    )
    stmt = (
        select(polymorphic)
        .where(PublicationModel.id == publication_id)
        .options(
            joinedload(polymorphic.categories),
            joinedload(polymorphic.BookModel.author),
        )
    )
    publication = await session.scalar(stmt)
    if publication is None:
        raise PublicationNotFoundError

    return publication


InjectPublicationFromPath: TypeAlias = Annotated[
    PublicationModel,
    Depends(_get_publication_from_id_in_path),
]

InjectUnionPublicationFromPath: TypeAlias = Annotated[
    UnionPublicationModel,
    Depends(_get_union_publication_from_id_in_path),
]
