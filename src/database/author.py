from typing import TYPE_CHECKING, final

from sqlalchemy.orm import Mapped, relationship

from src.core.db.types import Primary
from src.database import BaseModel

if TYPE_CHECKING:
    from src.database import BookModel


@final
class AuthorModel(BaseModel):
    __tablename__ = "author"

    id: Mapped[Primary[int]]
    name: Mapped[str]

    books: Mapped[list["BookModel"]] = relationship(back_populates="author")
