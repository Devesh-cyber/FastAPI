from fastapi import FastAPI
from database import create_table
from contextlib import asynccontextmanager
from routes.orders import router as order_route
from routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Database Started ...')
    create_table()
    yield

app = FastAPI(
    title='Dabbawala API',
    lifespan=lifespan
)

app.include_router(order_route)
app.include_router(stats_router)

@app.get('/', tags=['Health'])
def root():
    return {'Message' : 'Dabbawala API'}
