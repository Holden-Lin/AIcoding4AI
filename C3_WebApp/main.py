import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from C2_LLM_API.GenBookIntro import BookPromoter
import C2_LLM_API.learning_demos.openAI_demo as openAI_demo

from sse_starlette.sse import EventSourceResponse

gener = BookPromoter()
app = FastAPI()
# remember to set PYTHONPATH to the root directory and then run
templates = Jinja2Templates(directory="C3_WebApp/templates")
# Serving Static Files
app.mount("/static", StaticFiles(directory="C3_WebApp/static"), name="static")


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
async def generate_anything(book_name: str):
    completions = openAI_demo.gen(book_name)

    async def event_generator():
        for chunk in completions:
            if chunk is None:
                yield dict(data="Stream closed", event="stream-end")
                break
            yield dict(data=chunk)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
