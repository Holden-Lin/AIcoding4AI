import uvicorn
from fastapi import FastAPI
from C2_LLM_API.GenBookIntro import BookPromoter

gener = BookPromoter()
app = FastAPI()


@app.post("/gen")
def generate_book_intro(book_name):
    intro = gener.generate_intro(book_name)
    return intro


if __name__ == "__main__":
    uvicorn.run("GenBookIntroApp:app", reload=True, log_level="debug")
