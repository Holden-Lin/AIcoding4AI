import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from C2_LLM_API.GenBookIntro import BookPromoter
import asyncio

gener = BookPromoter()
app = FastAPI()
# remember to set PYTHONPATH to the root directory and then run
templates = Jinja2Templates(directory="W3/templates")
# Serving Static Files
app.mount("/static", StaticFiles(directory="W3/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Update the route to accept a JSON body with the structure defined by BookNameRequest
@app.get("/gen")
async def generate_book_intro(book_name: str):
    # Use the 'book_name' attribute from the request body
    intro = gener.generate_intro(book_name)

    return StreamingResponse(intro, media_type="text/event-stream")


# async def generate_book_intro(book_name: str):
#     async def intro_generator():
#         yield "data: Test message\n\n"
#         await asyncio.sleep(1)  # Sleep for 1 second
#         yield "data: Another test message\n\n"

#     return StreamingResponse(intro_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
