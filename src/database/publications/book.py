from typing import TYPE_CHECKING, ClassVar, final

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.types import Primary
from src.core.enums.publication_type import PublicationType
from src.database.publications.base import PublicationModel

if TYPE_CHECKING:
    from src.database import AuthorModel


@final
class BookModel(PublicationModel):
    __tablename__ = "book"

    id: Mapped[Primary[int]] = mapped_column(ForeignKey("publication.id"))

    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["AuthorModel"] = relationship(back_populates="books")
    author_name: AssociationProxy[str] = association_proxy(
        "author",
        "name",
    )

    __mapper_args__: ClassVar = {
        "polymorphic_identity": PublicationType.BOOK.value,
    }
