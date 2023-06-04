import aiofiles
import os

from fastapi import APIRouter, UploadFile, File, Response, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select

from .models import Audio
from logic import JWTManager
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from schemas import ResponseSchema
from .convertation import convert

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
# По стандарту используется PasswordBearer, но по заданию, сдесь не нужен пароль,
# на Swagger мы не сможем авторизоваться, но авторизация все еще работает
# проверить можно с помощью PostMan


@router.post('/upload')
async def upload(response: Response,
                uuid: str,
                token: str = Depends(oauth2_scheme),
                uploaded_file: UploadFile = File(...),
                session: AsyncSession = Depends(get_async_session)):
    """
    В задании не было указано создание пользователя с паролем, авторизация происходит
    с помощью хедера Authorization Bearer, для проверки, что это пользователь,
    владеющий аксес токеном мы декодируем токен и сравниваем с предъявленным uuid,
    используется встроенный класс OAuth2PasswordBearer, который просит на странице
    swagger пароль, проверить работоспособность можно в PostMan, скрины приложу
    """
    token = JWTManager.decode_token(token)
    filename, ext = uploaded_file.filename.split('.')
    file_location = f"files/{filename}.{ext}"

    if ext != 'wav':
        raise HTTPException(415, 'Uploaded file is not in .wav foormat')
    if token == {}:
        raise HTTPException(401, 'Token has expired')
    if token['uuid'] != uuid:
        raise HTTPException(401, 'UUID and token uuid are not equals')
    if os.path.exists(f'files/{filename}.mp3'):
        raise HTTPException(409, 'This file already uploaded')

    try:
        async with aiofiles.open(file_location, 'wb+') as file_object:
            await file_object.write(await uploaded_file.read())
        # Копирование wav файла на диск
        audio = Audio(title=f'{filename}')
        convert(filename, ext)
        session.add(audio)
        await session.commit()
        await session.refresh(audio)
        # Сохранение записи в бд и ее рефреш, для последующего возврата в ссылке ниже
        return ResponseSchema(status='OK',
                message=f"File {uploaded_file.filename} saved as {filename}.mp3",
                result=f'http://127.0.0.1:8000/Audio/record?user_id={uuid}&file_id={audio.uuid}')
    except IOError:
        response.status_code = 409
        return ResponseSchema(status='Error', message='Error in I/O operation')
    except Exception:
        response.status_code = 500
        return ResponseSchema(status='Error', message='Internal Server Error')


@router.get('/record')
async def get_record(user_id: str,
                     file_id: str,
                     token: str = Depends(oauth2_scheme),
                     session: AsyncSession = Depends(get_async_session)):
    """
    Проверяем, что введенный uuid совпадает с uuid в токене, отправляем файл,

    """
    token = JWTManager.decode_token(token)
    if token == {}:
        raise HTTPException(401, 'Token has expired')
    if token['uuid'] != user_id:
        raise HTTPException(401, 'UUID and token uuid are not equals')
    try:
        stmt = select(Audio).filter(Audio.uuid == file_id)
        audio = await session.execute(stmt)
        title = audio.mappings().first()['Audio'].title
        return FileResponse(path=f'files/{title}.mp3')
    except:
        raise HTTPException(500, 'Internal Server Error')
