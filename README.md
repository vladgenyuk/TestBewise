# TestBewise
Тестовое задание, 3 сервиса: скачивание воспросов из удаленного API https://jservice.io/api/random?count=1, 
регистрация пользвателя с UUID и JWT токеном, загрузка файлов и конвертация их из формата wav в формат mp3.

Использовались библиотеки: Fastapi, pydub, uvicorn, gunicorn, pydantic, typing, requests, SQLAlchemy, alembic.

Для запуска докер-компос файла нужно прописать команду **docker-compose up -d**, запустятся 2 сервиса,
на **localhost:8000/docs** можно посмотреть Swagger-docs проекта. 
Для запуска приложения без докер контейнера в корне, в файле .env нужно изменить
**DB_HOST=localhost** вместо **DB_HOST=db**, запустить постгрес командой **docker-compose up -d db**.

Чтобы проверить самому, нужно запустить **docker-compose up -d**, скачивание вопросов, регистрацию и авторизацию
можно проверить на **localhost:8000/docs**. Из-за специфики задачи, для регистрации пользователя, нам нужно отправить
только username.
Для проверки размещения и скачивания файлов, нужен Postman, т.к. использовался встроенный OAuth2PasswordBearer,
которому для работы на Swagger UI нужен пароль, которого нет. 

Для размещения файлов:
1) http://127.0.0.1:8000/Audio/upload
- Params: uuid; uuid_4
- Headers: Authorization; Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMThkOTg4OTktMzdjZC00MzgwLWJlZjYtZWNhY2NjZWY5ZWVkIiwidXNlcm5hbWUiOiJzdHJpbmciLCJleHAiOjE2ODU5MDU3MDd9.P4BKYZr9D5SSlKBMhHyIM5Be33C6MHALZavwIGR-fXM  
- Body: uploaded_file; game_over.wav

Для скачивания файлов (в отклике будет ссылка на скачивание, как на скрине):
2) <ins>Переходим по ссылке в отклике</ins>, автоматически подставятся user_id и file_id из БД.
- Headers: Authorization; Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMThkOTg4OTktMzdjZC00MzgwLWJlZjYtZWNhY2NjZWY5ZWVkIiwidXNlcm5hbWUiOiJzdHJpbmciLCJleHAiOjE2ODU5MDU3MDd9.P4BKYZr9D5SSlKBMhHyIM5Be33C6MHALZavwIGR-fXM  

Для показа работоспособности, добавил 4 скрина, на них виден ответ на скачивание вопросов и ответ на авторизацию,
Еще на 2-х видна работа с файлами.

В файлах с кодом оставил комментарии, чтобы лучше понимать, что там происходит, также важно прочитать комментарии под
эндпоинтами. 

Для загрузки:
-git reset --hard
-git pull https://github.com/vladgenyuk/TestBewise
