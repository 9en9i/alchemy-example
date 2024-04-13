from dataclasses import dataclass
from typing import ClassVar, final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, composite, mapped_column

from src.core.db.types import Primary
from src.core.enums.publication_type import PublicationType
from src.database.publications.base import PublicationModel


@dataclass
class Image:
    path: str
    name: str


@final
class MagazineModel(PublicationModel):
    __tablename__ = "magazine"

    id: Mapped[Primary[int]] = mapped_column(ForeignKey("publication.id"))
    cover: Mapped[Image] = composite(mapped_column("path"), mapped_column("name"))

    __mapper_args__: ClassVar = {
        "polymorphic_identity": PublicationType.MAGAZINE.value,
    }
