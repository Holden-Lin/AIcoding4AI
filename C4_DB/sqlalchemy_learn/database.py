# collections.abc is a module from the standard Python library providing abstract base classes \
# for the common objects we use daily in Python: iterators, generators, callables, sets, mappings, and so on. \
# They are mainly useful in advanced use cases where we need to implement new custom objects \
# that should behave like an iterator, generator, and so on. Here, we only use them as type hints.
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base

# Here, we set aiosqlite. In an async context, it’s necessary to specify the async driver we want to use. \
# Otherwise, SQLAlchemy will fall back to a standard, synchronous driver.
DATABASE_URL = "sqlite+aiosqlite:///chapter06_sqlalchemy.db"

engine = create_async_engine(DATABASE_URL)

# async_session_maker is a factory for creating new AsyncSession objects.
# TODO: how to understand factory
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# TODO: know about dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        # TODO: know more about yield
        # ensure the session remains open until the end of the request
        yield session


async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
