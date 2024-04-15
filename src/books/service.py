from collections.abc import Sequence
from typing import Final, final

from sqlalchemy import RowMapping, select
from sqlalchemy.orm import joinedload, selectinload, with_expression

from src.core.enums.comparison_operator import ComparisonOperator
from src.core.sevice import Service
from src.database import (
    AuthorModel,
    BookModel,
    CategoryModel,
    MagazineModel,
    PublicationCategoryAssociation,
    PublicationModel,
)
from src.database.favorite_publications import FavoritePublicationsModel

_MATCHING_OPERATOR: Final = {
    ComparisonOperator.eq: "==",
    ComparisonOperator.ne: "!=",
    ComparisonOperator.gt: ">",
    ComparisonOperator.ge: ">=",
    ComparisonOperator.lt: "<",
    ComparisonOperator.le: "<=",
}


@final
class BookService(Service):
    async def get_publication_with_categories(
        self,
        category_name: str | None,
        search_by_title: str | None,
        search_by_description: str | None,
        limit: int,
        offset: int,
    ) -> Sequence[PublicationModel]:
        stmt = select(PublicationModel).limit(limit).offset(offset)

        if category_name is not None:
            stmt = (
                stmt.join(
                    PublicationCategoryAssociation,
                    PublicationModel.id
                    == PublicationCategoryAssociation.publication_id,
                )
                .join(
                    CategoryModel,
                    CategoryModel.id == PublicationCategoryAssociation.category_id,
                )
                .where(CategoryModel.name == category_name)
            )

        if search_by_title is not None:
            stmt = stmt.where(PublicationModel.title.icontains(search_by_title))

        if search_by_description is not None:
            stmt = stmt.where(
                PublicationModel.description.icontains(search_by_description),
            )

        stmt = stmt.options(selectinload(PublicationModel.categories))
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_books(
        self,
        limit: int,
        offset: int,
    ) -> Sequence[BookModel]:
        stmt = (
            select(BookModel)
            .limit(limit)
            .offset(offset)
            .options(
                joinedload(BookModel.categories),
                joinedload(BookModel.author),
            )
        )

        result = await self.session.scalars(stmt)
        return result.unique().all()

    async def get_magazines(
        self,
        limit: int,
        offset: int,
    ) -> Sequence[MagazineModel]:
        stmt = (
            select(MagazineModel)
            .limit(limit)
            .offset(offset)
            .options(
                selectinload(MagazineModel.categories),
            )
        )

        result = await self.session.scalars(stmt)
        return result.all()

    async def get_favorite(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> Sequence[PublicationModel]:
        favorite_subquery = (
            select(1)
            .where(
                FavoritePublicationsModel.publication_id == PublicationModel.id,
                FavoritePublicationsModel.user_id == user_id,
            )
            .exists()
        )
        stmt = (
            select(PublicationModel)
            .limit(limit)
            .offset(offset)
            .options(
                with_expression(PublicationModel.is_favorite, favorite_subquery),
            )
        )

        result = await self.session.scalars(stmt)
        return result.all()

    async def get_categories(self, limit: int, offset: int) -> Sequence[RowMapping]:
        stmt = select(CategoryModel.name).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def get_authors(
        self,
        limit: int,
        offset: int,
        comp_op: ComparisonOperator | None,
        book_count: int | None,
    ) -> Sequence[AuthorModel]:
        stmt = select(AuthorModel).limit(limit).offset(offset)

        if comp_op and book_count:
            stmt = stmt.where(
                AuthorModel.book_count.op(_MATCHING_OPERATOR[comp_op])(book_count),
            )

        result = await self.session.scalars(stmt)
        return result.all()
