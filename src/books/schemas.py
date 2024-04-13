from typing import final

from pydantic import Field, computed_field

from src.core.schema import Schema


@final
class BookCategorySchema(Schema):
    name: str


@final
class ImageSchema(Schema):
    path: str
    name: str


@final
class AuthorSchema(Schema):
    name: str


class PublicationSchema(Schema):
    id: int
    title: str
    description: str | None
    likes: int


class PublicationWithCategoriesSchema(PublicationSchema):
    categories: list[BookCategorySchema]


class PublicationWithFavoriteSchema(PublicationSchema):
    is_favorite: bool


@final
class BookSchema(PublicationWithCategoriesSchema):
    author: AuthorSchema
    author_name: str


@final
class MagazineSchema(PublicationWithCategoriesSchema):
    cover: ImageSchema = Field(exclude=True)

    @computed_field
    def file(self) -> str:
        return f"{self.cover.path}/{self.cover.name}"


type UnionPublicationSchema = MagazineSchema | BookSchema
