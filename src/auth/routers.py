import datetime

from fastapi import APIRouter, Depends, Response
from sqlalchemy.exc import IntegrityError

from .schemas import UserCreate
from .models import User

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from logic import JWTManager, UserManager
from schemas import ResponseSchema, UUIDTokenSchema

router = APIRouter()


@router.post('/register')
async def register(request: UserCreate, response: Response,
                   session: AsyncSession = Depends(get_async_session)):
    """
    Регистрация пользователя и возврат его jwt токена, в задании было прописано,
    что к эндпоинту нужно обращаться с именем пользователя, пароль специально не делал
    """
    try:
        user = User(username=request.username)
        await UserManager.create_user(session=session, model=user)
        token = JWTManager.generate_token(data={'uuid': str(user.uuid),
                                                'username': str(user.username)},
                                          expire_delta=datetime.timedelta(minutes=15))

        response.status_code = 200
        return ResponseSchema(status='OK', message='Success',
                              result=UUIDTokenSchema(access_token=token,
                                                       token_type="Bearer",
                                                       uuid=user.uuid)).dict()
    except IntegrityError as e:
        response.status_code = 403
        return ResponseSchema(status='Error', message="User already exists").dict()
    except Exception as e:
        response.status_code = 500
        return ResponseSchema(status='Error', message='Internal Server Error').dict()


@router.post('/login')
async def login(request: UserCreate, response: Response,
                session: AsyncSession = Depends(get_async_session)):
    """
    Получение токена, в задании не оговаривалось наличие пароля, специально сделал
    регистрацию без него, при необходимости не составит труда добавить.
    """
    try:
        user = await UserManager.find_by_username(session=session, model=User,
                                            username=request.username)
        user = [dict(r._mapping)['User'] for r in user][0]
        # username это уникальное поле, поэтому вернуться может лишь 1 пользователь
        token = JWTManager.generate_token(data={'uuid': str(user.uuid),
                                                'username': str(user.username)},
                                          expire_delta=datetime.timedelta(minutes=15))
        response.status_code = 200
        return ResponseSchema(status='OK', message='success',
                              result=UUIDTokenSchema(access_token=token,
                                                       token_type="Bearer",
                                                       uuid=user.uuid)).dict()
    except IndexError as e:
        response.status_code = 404
        return ResponseSchema(status="Error", message='User with this username does not exist')
    except Exception as e:
        response.status_code = 500
        return ResponseSchema(status='Error', message='Internal Server Error').dict()

