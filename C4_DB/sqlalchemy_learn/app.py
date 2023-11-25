import contextlib
from collections.abc import Sequence

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .database import create_all_tables, get_async_session
from .models import Post


# lifespan is a context manager for FastAPI application to perform startup and shutdown events.
# To make sure our schema is created when our application starts, we must call this function the lifespan handler of FastAPI.
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    # This is used to divide the lifespan into two parts: before and after the yield. \
    # The code before the yield is executed when the application starts up, and the code after yield (if there were any)\
    #  would be executed when the application shuts down
    yield


app = FastAPI(lifespan=lifespan)


async def pagination(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=0),
) -> tuple[int, int]:
    capped_limit = min(100, limit)
    return (skip, capped_limit)


@app.post(
    "/posts", response_model=schemas.PostRead, status_code=status.HTTP_201_CREATED
)
async def create_post(
    # syntax: variable: type
    post_create: schemas.PostCreate,
    # Depends > dependency injection
    session: AsyncSession = Depends(get_async_session),
) -> Post:
    # ** change dict into keyword arguments so that they fit in db format
    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    return post


@app.get("/posts", response_model=list[schemas.PostRead])
async def list_posts(
    pagination: tuple[int, int] = Depends(pagination),
    session: AsyncSession = Depends(get_async_session),
) -> Sequence[Post]:
    skip, limit = pagination
    select_query = select(Post).offset(skip).limit(limit)
    result = await session.execute(select_query)

    return result.scalars().all()
