from pydantic import BaseModel, Field
from datetime import datetime


class Writing(BaseModel):
    id: int
    prompt: str
    answer: str
    creat_time: datetime = Field(default_factory=datetime.now)
    finish_time: datetime = Field(default_factory=datetime.now)
    prompt_tokens: int
    answer_tokens: int

    class Config:
        orm_mode = True


class WritingCreate(Writing):
    pass


class DeleteStatus(BaseModel):
    ok: bool
