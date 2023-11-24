
# To make sure our schema is created when our application starts, we must call this function the lifespan handler of FastAPI.
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield

@app.post("/posts", response_model=schemas.PostRead, status_code=status. HTTP_201_CREATED)

async def create_post(post_create: schemas.PostCreate, 
                      session: AsyncSession = Depends(get_async_session)
                      ) -> Post:

    post = Post(**post_create.dict())

    session.add(post)

    await session.commit()

    return post