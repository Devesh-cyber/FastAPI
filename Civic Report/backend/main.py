from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

# Allow the Vite dev server (and any other origin, for local/demo use)
# to call this API from the browser. Tighten allow_origins before
# deploying this for real.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded issue photos at /images/<filename> so the frontend
# can render them directly from image_path.
app.mount("/images", StaticFiles(directory="images"), name="images")

app.include_router(citizen_router)
app.include_router(issues_router)
app.include_router(analysis_router)

@app.get('/')
def root():
    return {'message': 'Civics Issue API Working ...'}