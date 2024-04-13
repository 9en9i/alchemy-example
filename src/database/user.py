from typing import final

from sqlalchemy.orm import Mapped

from src.core.db.base import BaseModel
from src.core.db.types import Primary


@final
class UserModel(BaseModel):
    __tablename__ = "user"

    id: Mapped[Primary[int]]
    email: Mapped[str]
