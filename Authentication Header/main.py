from fastapi import FastAPI
from routes.books import router as books_router
from routes.user import router as user_router
from contextlib import asynccontextmanager
from database import create_table

@asynccontextmanager
async def lifespan(api: FastAPI):
    create_table()
    print('Database Created ...')
    yield


app = FastAPI(
    title='Kitaab Exchange API',
    description='A simple API for exchnaging used books',
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(books_router)

@app.get('/')
def root():
    return {'message': 'Kitaab API'}