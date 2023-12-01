import uvicorn, contextlib
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from C2_LLM_API.GenBookIntro import BookPromoter
import C2_LLM_API.learning_demos.openAI_demo as openAI_demo
from common.count_tokens import count_tokens

from sse_starlette.sse import EventSourceResponse

# use absolute import in main script
from database import schemas, crud
from database.database import SessionLocal, create_tables
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from typing import List

import traceback


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
gener = BookPromoter()
# remember to set PYTHONPATH to the root directory and then run
templates = Jinja2Templates(directory="C4_DB/templates")
# Serving Static Files
app.mount("/static", StaticFiles(directory="C4_DB/static"), name="static")


async def get_db():
    db = SessionLocal()
    try:
        print("* creating db session")
        yield db
    finally:
        print("* closing db session")
        await db.close()


# async def get_db():
#     print("* creating db session")
#     async with SessionLocal() as session:
#         yield session


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Update the route to accept a JSON body with the structure defined by BookNameRequest
@app.get("/genbook")
async def generate_book_intro(book_name: str):
    # Use the 'book_name' attribute from the request body
    intro = gener.generate_intro(book_name)

    return StreamingResponse(intro, media_type="text/event-stream")


@app.get("/gen")
async def generate_anything(
    user_input: str, user_ip: str, db: AsyncSession = Depends(get_db)
):
    # Create initial entry with prompt and create_time
    writing_create = schemas.WritingCreate(
        prompt=user_input,
        creat_time=datetime.now(),
        prompt_tokens=count_tokens(user_input),
        user_ip=user_ip,
    )
    try:
        print("* creating database transaction")
        writing_entry = await crud.create_writing(db, writing_create)
    except Exception as e:
        traceback_str = "".join(traceback.format_tb(e.__traceback__))
        error_msg = f"{e.__class__.__name__}: {e}\n{traceback_str}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=str(e))

    print("* generating model output")
    completions = openAI_demo.gen(user_input)

    async def event_generator():
        # Send the ID as the first event
        yield dict(data=str(writing_entry.id), event="init-id")
        print("* yielding output")

        for chunk in completions:
            if chunk is None:
                yield dict(data="Stream closed", event="stream-end")
                break
            yield dict(data=chunk)

    return EventSourceResponse(event_generator())


@app.put("/update/{writing_id}", response_model=schemas.Writing)
async def update_writing_endpoint(
    writing_id: int,
    update_data: schemas.WritingUpdate,
    db: AsyncSession = Depends(get_db),
):
    print("* updating db after generation")
    answer_tokens = count_tokens(update_data.answer)
    update_data.answer_tokens = answer_tokens
    update_data.finish_time = datetime.now()

    updated_writing = await crud.update_writing(db, writing_id, update_data)
    return updated_writing


@app.get("/get_history", response_model=List[schemas.WritingResponse])
async def get_history(user_ip: str, db: AsyncSession = Depends(get_db)):
    history = await crud.get_writings_by_ip(db, user_ip=user_ip)
    return history


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
