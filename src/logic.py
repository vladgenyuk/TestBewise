import datetime
import jwt

from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar

from database import get_async_session
from config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET, ALGORITHM
from auth.models import User


T = TypeVar('T')


class UserManager():

    @staticmethod
    async def find_by_username(username: str, model: Generic[T],
                         session: AsyncSession):
        stmt = select(User).where(model.username == username)
        return await session.execute(stmt)


    @staticmethod
    async def create_user(model: Generic[T],
            session: AsyncSession):
        session.add(model)
        await session.commit()
        await session.refresh(model)


class JWTManager():

    @staticmethod
    def generate_token(data: dict, expire_delta=datetime.timedelta(minutes=1)):
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.datetime.utcnow() + expire_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
        # expire = expire.timestamp()
        to_encode.update({'exp': expire})
        encode_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
        return encode_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            decode_token = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
            return decode_token if decode_token['exp'] >= datetime.datetime.utcnow().timestamp() else None
        except:
            return {}
