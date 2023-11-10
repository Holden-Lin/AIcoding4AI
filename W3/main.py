import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from C2_LLM_API.GenBookIntro import BookPromoter

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
    print("* generated text returned")

    return StreamingResponse(intro, media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
