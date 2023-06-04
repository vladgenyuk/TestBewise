from fastapi import FastAPI


from quiz.routers import router as quiz_router
from auth.routers import router as auth_router
from audio.routers import router as audio_router


app = FastAPI()


@app.get('/')
async def hello():
    return {"Hello": "World"}


app.include_router(quiz_router,
                   prefix='/Quiz',
                   tags=['Quiz'])

app.include_router(auth_router,
                   prefix='/Auth',
                   tags=['Auth'])

app.include_router(audio_router,
                   prefix='/Audio',
                   tags=['Audio'])