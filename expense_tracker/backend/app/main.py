from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.expense_router import router as expense_router
from app.analyze_router import router as analyze_router
from app.operation_router import router as operation_router
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

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(expense_router)
app.include_router(analyze_router)
app.include_router(operation_router)

@app.get('/')
def root():
    return {'message' : 'Welcome to the Expense Tracker Page'}