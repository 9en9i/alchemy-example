from typing import final

from fastapi import HTTPException
from starlette import status


@final
class PublicationNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Publication not found",
        )
