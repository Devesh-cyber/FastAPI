from fastapi import FastAPI
from app.router import router as expense_router
from contextlib import asynccontextmanager
from app.database import create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Database Created')
    create_table()
    yield

app = FastAPI(
    title='Expense Tracker',
    description='The API for managing all the expenses',
    lifespan=lifespan
)


app.include_router(expense_router)

@app.get('/')
def root():
    return {'message' : 'Welcome to the Expense Tracker Page'}