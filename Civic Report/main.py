from fastapi import FastAPI
from database import create_tables
from contextlib import asynccontextmanager
from routes.citizen import router as citizen_router
from routes.issues import router as issues_router
from routes.analysis import router as analysis_router
from models.citizen import Citizens
from models.issues import Issues

@asynccontextmanager
async def lifespan(api: FastAPI):
    create_tables()
    print('Database Created ...')
    yield
    print('Database Shutting down')

app = FastAPI(
    title='Civics Issue API',
    lifespan=lifespan
)

app.include_router(citizen_router)
app.include_router(issues_router)
app.include_router(analysis_router)

@app.get('/')
def root():
    return {'message': 'Civics Issue API Working ...'}