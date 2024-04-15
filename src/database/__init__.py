from src.core.db.base import BaseModel
from src.database.author import AuthorModel
from src.database.category import CategoryModel
from src.database.category__publication import PublicationCategoryAssociation
from src.database.favorite_publications import FavoritePublicationsModel
from src.database.publications.base import PublicationModel
from src.database.publications.book import BookModel
from src.database.publications.magazine import MagazineModel
from src.database.user import UserModel

type UnionPublicationModel = BookModel | MagazineModel

__all__ = (
    "UnionPublicationModel",
    "BaseModel",
    "AuthorModel",
    "BookModel",
    "CategoryModel",
    "PublicationModel",
    "MagazineModel",
    "UserModel",
    "PublicationCategoryAssociation",
    "FavoritePublicationsModel",
)
