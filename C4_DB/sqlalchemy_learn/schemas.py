from datetime import datetime
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str
    content: str
    # Field is used to provide extra validation and metadata for Pydantic models
    # refer to https://docs.pydantic.dev/latest/api/fields/
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        # With ORM, however, we access the properties like an object – that is, by using dot notation (o.title). \
        # Enabling ORM mode allows Pydantic to use this style.
        orm_mode = True


class PostPartialUpdate(BaseModel):
    #  str | None means that the type of the title and content attributes can be either a str (string) or None
    # a syntax after python 3.10
    title: str | None = None
    content: str | None = None


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    # TODO: can add new field to base class?
    id: int
