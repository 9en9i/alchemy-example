from typing import final

from sqlalchemy import SQLColumnExpression, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, relationship

from src.core.db.types import Primary
from src.database import BaseModel, BookModel


@final
class AuthorModel(BaseModel):
    __tablename__ = "author"

    id: Mapped[Primary[int]]
    name: Mapped[str]

    books: Mapped[list["BookModel"]] = relationship(
        back_populates="author",
        lazy="selectin",
    )

    @hybrid_property
    def book_count(self) -> int:
        return len(self.books)

    @book_count.inplace.expression
    @classmethod
    def _book_count_query(cls) -> SQLColumnExpression[int]:
        return (
            select(func.count(BookModel.id))
            .where(BookModel.author_id == cls.id)
            .label("book_count")
        )
