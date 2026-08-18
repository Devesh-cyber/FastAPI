from fastapi import FastAPI
from app.routes.analysis import router as analysis_router

app = FastAPI(
    title='Netra Vision',
    version='1.0.0',
    description='AI_powered crop disease detection using Gemini'
)

app.include_router(analysis_router)

@app.get('/')
def root():
    return {
        'app' : 'netra-vision',
        'endpoints' : {
            'POST /analyse' : "Uploads the image",
            'POST /analyse/batch' : "Uploads the images in batch",
            'GET /analyse' : "Retreievs a list of all analysis",
            'GET /analyse/{analysis_id}' : "Retreieves analysis by id"
        } 
    }