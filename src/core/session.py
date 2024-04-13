from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.settings import settings

engine = create_async_engine(
    str(settings.SQLALCHEMY_URI),
    pool_size=20,
    max_overflow=10,
)

local_session = async_sessionmaker(engine)
