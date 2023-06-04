import datetime

import requests
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Questions


# Не использовал аннотацию только потому, что в функцию
# могут прилетать разные виды данных
# и функция может отдать разные данные (dict, list)
def validate_data(data):# Функция для валидации данных
    validated_data = [{
        'id': item.get('id'),
        'question': item.get('question'),
        'answer': item.get('answer'),
        'created_at': datetime.datetime.strptime(item.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ'),
        'added_at': datetime.datetime.now(),
        'value': item.get('value'),
    } for item in data]
    return validated_data


def partial_validate_data(data):# Функция для валидации данных
    # Поле ID в этой фк делится на 20, в бд может быть максимум 19 записей
    # Эта функция показывает докачку записей, если попалась запись с одинаковым ID
    # Это все сделал лишь для примера
    validated_data = [{
        'id': item.get('id') % 20 + 1,
        'question': item.get('question'),
        'answer': item.get('answer'),
        'created_at': datetime.datetime.strptime(item.get('created_at'), '%Y-%m-%dT%H:%M:%S.%fZ'),
        'added_at': datetime.datetime.now(),
        'value': item.get('value'),
    } for item in data]
    return validated_data


async def insert_all(session: AsyncSession,
               validated_data):
     # Пытаемся вставить в бд сразу question_num записей
    stmt = insert(Questions).values(validated_data)
    await session.execute(stmt)
    await session.commit()


async def insert_by_one(session: AsyncSession,
                  question_num: int,
                  validated_data,
                  validate_function,
                  url: str):
    count = 0
    try_count = 0
    while count < question_num:
        print(try_count)
        if try_count >= 100:
            return
        # Если не вышло, пытаемся вставить запись,
        # если не получилось, обращаемся к юрл за новой,
        # пока не найдем уникальную, которой нет в бд.
        # Повторяем операцию пока не вставим question_num записей
        # или не превысим предел попыток (100)
        try:
            try_count += 1
            stmt = insert(Questions).values(validated_data[count])
            await session.execute(stmt)  # Тут мы начинаем транзакцию
            await session.commit()
            count += 1
        except Exception as e:
            await session.rollback()  # Тут, если ее не прервать, мы не сможем начать новую
            data = requests.get(url + '1').json()  # Запрос одной новой записи
            validated_data[count] = validate_function(data)[0]
