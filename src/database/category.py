from typing import TYPE_CHECKING, final

from sqlalchemy.orm import Mapped, relationship

from src.core.db.types import Primary
from src.database import BaseModel

if TYPE_CHECKING:
    from src.database import PublicationModel


@final
class CategoryModel(BaseModel):
    __tablename__ = "category"

    id: Mapped[Primary[int]]
    name: Mapped[str]

    publications: Mapped[list["PublicationModel"]] = relationship(
        secondary="category__publication",
        back_populates="categories",
    )
