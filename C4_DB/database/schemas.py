# schemas.py
from pydantic import BaseModel


class WritingCreate(BaseModel):
    tip: str
    content: str


class Writing(BaseModel):
    id: int
    tip: str
    content: str

    class Config:
        orm_mode = True


class DeleteStatus(BaseModel):
    ok: bool
