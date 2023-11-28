# schemas.py regulates the expectations of fastapi request and response
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Writing(BaseModel):
    id: Optional[int]
    prompt: str
    answer: Optional[str] = None
    creat_time: Optional[datetime] = None
    finish_time: Optional[datetime] = None
    prompt_tokens: Optional[int] = None
    answer_tokens: Optional[int] = None

    class Config:
        # new version: from_attributes=True
        orm_mode = True  # Use orm_mode for compatibility with older versions


class WritingCreate(BaseModel):
    prompt: str
    user_ip: Optional[str] = None
    creat_time: datetime
    prompt_tokens: int
    # Exclude 'id', 'answer', 'answer_tokens', 'finish_time'


class WritingResponse(Writing):
    pass
    # This can be used for responses, including all fields
