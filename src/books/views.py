from typing import cast

from fastapi import APIRouter

from src.books.depends import InjectPublicationFromPath, InjectUnionPublicationFromPath
from src.books.schemas import (
    BookCategorySchema,
    BookSchema,
    MagazineSchema,
    PublicationSchema,
    PublicationWithCategoriesSchema,
    PublicationWithFavoriteSchema,
    UnionPublicationSchema,
)
from src.books.service import BookService
from src.core.depends import Inject, InjectFromQuery
from src.core.pagination import LimitOffsetPagination

router = APIRouter(prefix="/publications", tags=["Publications"])


@router.get("/base/{publication_id}")
async def get_base_publication_by_id(
    publication: InjectPublicationFromPath,
) -> PublicationSchema:
    # тут можно что-то более явное сделать, вместо BookSchema.cast()
    return PublicationSchema.cast(publication)


@router.get("/union/{publication_id}")
async def get_union_publication_by_id(
    publication: InjectUnionPublicationFromPath,
) -> UnionPublicationSchema:
    return cast(UnionPublicationSchema, publication)


@router.get("/")
async def get_publication_with_categories(
    service: Inject[BookService],
    pagination: Inject[LimitOffsetPagination],
    category_name: InjectFromQuery[str | None] = None,
    search_by_title: InjectFromQuery[str | None] = None,
    search_by_description: InjectFromQuery[str | None] = None,
) -> list[PublicationWithCategoriesSchema]:
    books = await service.get_publication_with_categories(
        category_name,
        search_by_title,
        search_by_description,
        pagination.limit,
        pagination.offset,
    )
    return PublicationWithCategoriesSchema.cast(books)


@router.get("/book")
async def get_books(
    service: Inject[BookService],
    pagination: Inject[LimitOffsetPagination],
) -> list[BookSchema]:
    books = await service.get_books(
        pagination.limit,
        pagination.offset,
    )
    return BookSchema.cast(books)


@router.get("/magazine")
async def get_magazine(
    service: Inject[BookService],
    pagination: Inject[LimitOffsetPagination],
) -> list[MagazineSchema]:
    books = await service.get_magazines(
        pagination.limit,
        pagination.offset,
    )
    return MagazineSchema.cast(books)


@router.get("/get_with_favorite")
async def get_with_favorite(
    service: Inject[BookService],
    pagination: Inject[LimitOffsetPagination],
    user_id: InjectFromQuery[int],
) -> list[PublicationWithFavoriteSchema]:
    publications = await service.get_favorite(
        user_id,
        pagination.limit,
        pagination.offset,
    )
    return PublicationWithFavoriteSchema.cast(publications)


@router.get("/categories")
async def get_categories(
    service: Inject[BookService],
    pagination: Inject[LimitOffsetPagination],
) -> list[BookCategorySchema]:
    publications = await service.get_categories(
        pagination.limit,
        pagination.offset,
    )
    return BookCategorySchema.cast(publications)
