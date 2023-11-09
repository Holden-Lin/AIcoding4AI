import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from C2_LLM_API.GenBookIntro import BookPromoter

# Instantiate your BookPromoter
gener = BookPromoter()
app = FastAPI()
templates = Jinja2Templates(directory="W3/templates")
# Serving Static Files
app.mount("/static", StaticFiles(directory="W3/static"), name="static")


# Define a Pydantic model to strictly type-check the incoming request body
class BookNameRequest(BaseModel):
    book_name: str


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Update the route to accept a JSON body with the structure defined by BookNameRequest
@app.post("/gen")
async def generate_book_intro(request: BookNameRequest):
    # Use the 'book_name' attribute from the request body
    intro = gener.generate_intro(request.book_name)
    print("* generated text returned")

    return {"intro": intro}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
