from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models import Base

# Here, we set aiosqlite. In an async context, it’s necessary to specify the async driver we want to use. \
# Otherwise, SQLAlchemy will fall back to a standard, synchronous driver.
DATABASE_URL = "sqlite+aiosqlite:///chapter06_sqlalchemy.db"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# TODO: know about dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        # TODO: know more about yield
        # ensure the session remains open until the end of the request
        yield session