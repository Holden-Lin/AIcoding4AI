from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ///: The triple forward slashes indicate to SQLAlchemy that it should expect a relative file path to follow. \
# This is a standard part of the URL format for SQLAlchemy.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./database1125.db"

# Setting check_same_thread to False disables this check, allowing multiple threads to use the same connection. \
# This is necessary in an asynchronous environment like FastAPI, where multiple asynchronous tasks \
# (which may run in different threads) need to access the database concurrently.
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


# to create tables in your database initialization process.
async def create_tables():
    async with engine.begin() as conn:
        # This will create all tables defined in your Base's subclasses
        await conn.run_sync(Base.metadata.create_all)


# autocommit :
# This is a common practice in web applications, as it allows for better control over database transactions, \
# enabling you to bundle several operations together into a single transaction and commit them all at once.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
