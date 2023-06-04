import uuid

from sqlalchemy import Column, String, UUID
from database import Base, metadata


class Audio(Base):
    __tablename__ = "audio"

    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
