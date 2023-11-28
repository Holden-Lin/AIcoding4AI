from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from .database import Base


class Writing(Base):
    __tablename__ = "writings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_ip = Column(String, nullable=True)
    prompt = Column(String, nullable=False)
    answer = Column(Text, nullable=True)
    creat_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    finish_time = Column(DateTime, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    answer_tokens = Column(Integer, nullable=True)
