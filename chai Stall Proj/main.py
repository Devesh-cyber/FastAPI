from fastapi import FastAPI, HTTPException, Query
from data import menu_items
from model import MenuItems, MenuResponse

app = FastAPI(
    title='Chai Point API',
    description='This is a API point for Chai to access API from mobile and displays'
)

@app.get('/')
def root():
    return {'message' : 'Welcome to the Root page for Chai Point'}

@app.get('/menu', response_model=MenuResponse)
def get_menu_items(category : str | None = Query(None, description='Filter by chai, coffee or combo')):
    if category:
        filtered = [item for item in menu_items if item['category'].lower() == category.lower()]
        if filtered:
            return MenuResponse(count = len(filtered), items = filtered)
        raise HTTPException(status_code=404, detail=f'No cateogey {category} found in menu items')
    return MenuResponse(count=len(menu_items), items=menu_items)
        

@app.get('/menu/{id}', response_model=MenuItems)
def get_menu_item_by_id(id : int):
    for item in menu_items:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f'The menu item with id {id} is not found')
        