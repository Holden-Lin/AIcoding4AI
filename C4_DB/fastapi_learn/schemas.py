from datetime import datetime
from pydantic import BaseModel, Field

class PostBase(BaseModel):

    title: str
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)
    
    class Config:
        # With ORM, however, we access the properties like an object – that is, by using dot notation (o.title). \
        # Enabling ORM mode allows Pydantic to use this style.
        orm_mode = True

class PostPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int