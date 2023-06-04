from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class UserRead(BaseModel):
    id: int
    uuid: UUID = Field(default_factory=uuid4)
    username: str


class UserCreate(BaseModel):
    username: str
