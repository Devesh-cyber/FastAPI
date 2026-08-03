from fastapi import FastAPI
from database import create_table
from contextlib import asynccontextmanager
from router.reviews import router as review__router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    print('Database tables created')
    yield
    # Shutdown Logic
    print('Shutting Down the app')

app = FastAPI(
    title='Rangmanch Reviews API',
    description='Thathre reviews API for Pune Rangmanch',
    lifespan=lifespan
)

app.include_router(review__router)
@app.get('/')
def root():
    return {'message' : 'Welocme to Pune Rangmanch'}