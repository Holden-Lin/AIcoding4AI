# main.py
# fastapi uvicron
# 小红书文案生成器

# 引入html，css,js
# 静态文件

from fastapi import FastAPI, Request, Response, Depends
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from database import crud, models, schemas
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
import zhipuai

app = FastAPI()

# 请去智普AI官网申请自己的api_key：ww.zhipuai.cn
zhipuai.api_key = ""

# 用orm生成数据库的表格
models.Base.metadata.create_all(bind=engine)


# 抽象生成session的过程，包括生成session和关闭session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 生成文案的提示词的数据结构
class Item(BaseModel):
    prompt: str | None = ""


# 模板引擎 templates
templates = Jinja2Templates(directory="templates")

# 创建静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    # 获取数据库中，writings表中的数据
    writings = crud.get_writings(db)
    return templates.TemplateResponse(
        "index.html", {"request": request, "writings": writings}
    )


@app.post("/api/generate")
async def generate(item: Item):
    # 请求智普AI的API，并且以stream形式
    def stream():
        response = zhipuai.model_api.sse_invoke(
            model="chatglm_pro",
            prompt=[
                {
                    "role": "user",
                    "content": f"你好，请按照{item.prompt}的要求，生成小红书文案，要求包括三部分：标题、内容和标签",
                }
            ],
            top_p=0.7,
            temperature=0.9,
        )

        for event in response.events():
            yield event.data

    return StreamingResponse(stream())


# 创建新的数据
@app.post("/api/create", response_model=schemas.Writing)
def create_writing(writing: schemas.WritingCreate, db: Session = Depends(get_db)):
    result = crud.create_writing(db=db, writing=writing)
    return result


# 删除数据
@app.delete("/api/delete/{id}", response_model=schemas.DeleteStatus)
async def delete_writing(id: int, db: Session = Depends(get_db)):
    result = crud.delete_writing(db=db, id=id)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, log_level="info")
