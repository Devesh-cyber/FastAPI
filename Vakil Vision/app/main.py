from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def startup_event():
    init_db()

app = FastAPI(
    title='Vakeel Contracts API',
    description='AI-Powered Contract Analysis using Gemini',
    version='1.0.0'
)

@app.get('/')
def root():
    return {
        'app' : 'Vakeel Contract API',
        'version': '1.0.0',
        'endpoints' : {
            "POST /contaract/upload" : 'Upload a PDF or txt contract for analysis',
            'GET /contracts/' : 'Retrieve a list of all uploaded contracts',
            'GET /contacts/{id}' : 'Retrieves details of a specific contract by ID',
            'POST /analysis/analyse/{id}' : 'Analyze a contract using AI and return insights',
            'GET /analysis/{analysis_id}' : 'Retrieve the reults of a specific analysis by ID',
            'GET /analysis/contract/{contract_id}' : 'Retrieve the list of all analyses performed for a specific id'

        }
    }