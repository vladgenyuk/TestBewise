import uuid

from sqlalchemy import Column, String, Integer, UUID
from database import Base, metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    username = Column(String, unique=True)