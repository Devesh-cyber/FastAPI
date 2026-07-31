from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def show_data():
    """Show the data"""
    return [
        {"order" : "Butter Chicken", "status" : "Ordered"},
        {"order" : "Panner Tikka", "status" : "Preparing"},
        {"order" : "Biryani", "status" : "Ordered"},
    ]