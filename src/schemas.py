from pydantic import BaseModel, Field
from typing import Dict, Optional, TypeVar
from fastapi import File, UploadFile

# Создал данный файл для удобства форматирования Respons'ov

T = TypeVar('T')
# Означает, что в результате может быть любой тип данных


class Parameter(BaseModel):
    data: Dict[str, str] = None


class RequestSchema(BaseModel):
    parameter: Parameter = Field(...)


class ResponseSchema(BaseModel):
    status: str
    message: str
    result: Optional[T] = None


class UUIDTokenSchema(BaseModel):
    uuid: T
    access_token: str
    token_type: str


