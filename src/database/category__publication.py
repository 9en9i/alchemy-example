from typing import final

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db.types import Primary
from src.database import BaseModel


@final
class PublicationCategoryAssociation(BaseModel):
    __tablename__ = "category__publication"

    publication_id: Mapped[Primary[int]] = mapped_column(ForeignKey("publication.id"))
    category_id: Mapped[Primary[int]] = mapped_column(ForeignKey("category.id"))
