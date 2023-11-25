from sqlalchemy import create_engine
from sqlalchemy.orm import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

# 定义数据库的连接URL
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:./database1125.db"

# Setting check_same_thread to False disables this check, allowing multiple threads to use the same connection. \
# This is necessary in an asynchronous environment like FastAPI, where multiple asynchronous tasks \
# (which may run in different threads) need to access the database concurrently.
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# autocommit :
# This is a common practice in web applications, as it allows for better control over database transactions, \
# enabling you to bundle several operations together into a single transaction and commit them all at once.
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
