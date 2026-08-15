from fastapi import FastAPI
from app.database import create_tables
from contextlib import asynccontextmanager
from app.routes.user import router as user_router
from app.routes.contract import router as contract_router
from app.routes.analysis import router as analysis_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Database Created ...')
    create_tables()
    yield


app = FastAPI(
    title='Vakeel Vision API',
    description='This is Vakeel Vision where lawyer uploads a contract and get a detailed report.',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(user_router)
app.include_router(contract_router)
app.include_router(analysis_router)


@app.get('/')
def root():
    return {
        'message' : 'This is Vakeel vision API',
        'status' : 'success'
    }

