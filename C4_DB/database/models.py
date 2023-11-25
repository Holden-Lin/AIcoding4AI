from sqlalchemy import Column, Integer, String, Text, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 使用declarative_base创建一个Base类
# declarative_base是一个工厂函数，它为声明式类定义创建一个新的Base类。
# 你的模型类（即数据库表的模型）通常会继承这个Base类。
# 这种方式允许你使用面向对象的方式来定义数据库的表和关系。
class Base(DeclarativeBase):
    pass


# 定义数据库中的表
class Writing(Base):
    # 表名
    __tablename__ = "writings"

    # 表结构
    # id = Column(Integer, primary_key=True, index=True)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    prompt: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    creat_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    finish_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    prompt_tokens: Mapped[int] = mapped_column(Integer)
    answer_tokens: Mapped[int] = mapped_column(Integer)
