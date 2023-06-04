import requests

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

from .models import Questions
from .logic import validate_data, partial_validate_data, insert_by_one, insert_all

from schemas import ResponseSchema, RequestSchema
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.delete('/delete_all_questions', tags=['Quiz'])
async def delete_questions(session: AsyncSession = Depends(get_async_session)):
    """
    Просто удаляет все записи в бд, для простоты использования,
    чтобы не пришлось вручную это делать
    """
    stmt = delete(Questions)
    print(stmt)
    await session.execute(stmt)
    await session.commit()
    return ResponseSchema(status='OK', message="All users questions are deleted").dict()


@router.get('/questions', tags=['Quiz'])
async def get_all_questions(session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(Questions)
        result = await session.execute(stmt)
        ret = [dict(r._mapping)['Questions'] for r in result]
        return ResponseSchema(status="OK", message="View All questions", result=ret).dict()
    except Exception as e:
        return ResponseSchema(status="Error", message='Internal Server Error')


@router.post('/{question_num}', tags=['Quiz'])
async def quiz(question_num: int,
               session: AsyncSession = Depends(get_async_session)):
    """
        https://jservice.io/api/random?count=
        Имеет лимит в 100 записей за раз
        поэтому вводить числа больше 100 не имеет смысла, я пытался скачать
        100000 записей циклом и получил 429 too many requests.
        Также я не совсем понял, что имелось в виду вернуть предыдущий сохраненный объект.
        В ответе получаем последний добавленный объект (по дате added_at) (строка 56).
    """
    url = f"https://jservice.io/api/random?count="
    data = requests.get(url + str(question_num)).json()
    validated_data = validate_data(data)
    ret = await session.execute(text('select * from questions order by added_at desc limit 1;'))
    ret = ret.mappings().first() # Получение результата из курсора (итератора) строки выше
    if ret is None:
        ret = "NO notes in db"
    try:
        await insert_all(session, validated_data)
        return ResponseSchema(status="OK", message=f"Inserted {question_num} questions", result=ret).dict()
    except IntegrityError:
        # pass
        await insert_by_one(session, question_num, validated_data, validate_data, url)
        return ResponseSchema(status="OK", message=f"Inserted questions", result=ret).dict()
    except Exception:
        return ResponseSchema(status="Error", message='Internal Server Error or Error with CORS (429 status code)')


@router.post('/partial/{question_num}', tags=['Quiz'])
async def partial_quiz(question_num: int,
               session: AsyncSession = Depends(get_async_session)):
    """
        https://jservice.io/api/random?count=
        Имеет лимит в 100 записей за раз
        поэтому вводить числа больше 100 не имеет смысла,
        данный эндпоинт то же самое, что и предыдущий, но позволяет продемонстрировать
        докачку записей, если нашли записи с одинаковым ID, может
        долго работать, т.к. записи запрашиваются с URL по одной, количество попыток - 100,
        определено мною
    """
    url = f"https://jservice.io/api/random?count="
    data = requests.get(url + str(question_num)).json()
    validated_data = partial_validate_data(data)
    ret = await session.execute(text('select * from questions order by added_at desc limit 1;'))
    ret = ret.mappings().first() # Получение результата из курсора (итератора) строки выше
    if ret is None:
        ret = "NO notes in db"
    try:
        await insert_all(session, validated_data)
        return ResponseSchema(status="OK", message=f"Inserted {question_num} questions", result=ret).dict()
        # В данной функции с большой вероятностью попадется дубликат, т.к. мы делим
        # с остатком на 20, скорее всего выполнится блок Except, необходимо запустить
        # данную функцию несколько раз
    except IntegrityError:
        await insert_by_one(session, question_num, validated_data, partial_validate_data, url)
        return ResponseSchema(status="OK", message=f"Inserted questions", result=ret).dict()
    except Exception:
        return ResponseSchema(status="Error", message='Internal Server Error or Error with CORS (429 status code)')
