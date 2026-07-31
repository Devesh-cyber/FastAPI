from fastapi import FastAPI

app = FastAPI(
    title='Chai Point API',
    description='This is a API point for Chai to access API from mobile and displays'
)

@app.get('/')
def root():
    return {'message' : 'Welcome to the Root page for Chai Point'}

