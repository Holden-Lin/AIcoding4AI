# web http server
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "Hello World"


if __name__ == "__main__":
    # main is the script name,app is the fastapi app name
    # reload: server to automatically restart after code changes
    # log_level: could be "debug"
    uvicorn.run("main:app", reload=True, log_level="info")
