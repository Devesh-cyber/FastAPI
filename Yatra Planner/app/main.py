from fastapi import FastAPI
from app.routes.planner import router as planner_router

app = FastAPI(
    title='Yatra Planner API',
    description='Yatra API uses SSE and continuesly take streaming data form server',
    version='1.0.0'
)

app.include_router(planner_router)

@app.get('/')
def root():
    return {
        'app' : 'Yatra Planner App',
        'version' : '1.0.0',
        'endpoints' : {
            'POST /plan' : 'Create a travel plan (Aggregated)',
            'GET /plan/stream' : 'Stream a travel plan (SSE)',
            'GET /plan/cache-stats' : 'View Cache Statistics for travel plans',
            'DELETE /plan/cache' : 'Clear Cach for travel plan'
        }

    }