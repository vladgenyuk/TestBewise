from sqlalchemy import Column, Integer, String, DateTime, func
from database import metadata, Base


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True)
    answer = Column(String, unique=True)
    value = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    added_at = Column(DateTime, default=func.now())
