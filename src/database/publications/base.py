from typing import TYPE_CHECKING, ClassVar, cast

from sqlalchemy import func, select
from sqlalchemy.orm import (
    Mapped,
    MappedSQLExpression,
    column_property,
    mapped_column,
    query_expression,
    relationship,
)

from src.core.db.base import BaseModel
from src.core.db.mixins import CRUDInfoMixin
from src.core.db.types import Primary
from src.core.enums.publication_type import PublicationType
from src.database.favorite_publications import FavoritePublicationsModel

if TYPE_CHECKING:
    from src.database import CategoryModel


class PublicationModel(BaseModel, CRUDInfoMixin):
    __tablename__ = "publication"

    id: Mapped[Primary[int]] = (
        mapped_column()
    )  # тут нужен mapped_column для column_property

    title: Mapped[str]
    description: Mapped[str | None]

    categories: Mapped[list["CategoryModel"]] = relationship(
        secondary="category__publication",
        back_populates="publications",
    )

    likes: MappedSQLExpression[int] = column_property(
        select(func.count())
        .where(FavoritePublicationsModel.publication_id == id)
        .correlate_except(FavoritePublicationsModel)
        .scalar_subquery(),
    )

    # query_expression функция, поэтому не поддерживает параметр типа и нужен cast,
    # но для 3.13 есть pep 718
    is_favorite: MappedSQLExpression[bool] = cast(
        MappedSQLExpression[bool],
        query_expression(),
    )

    publication_type: Mapped[PublicationType]

    __mapper_args__: ClassVar = {
        "polymorphic_abstract": True,
        "polymorphic_on": "publication_type",
    }
