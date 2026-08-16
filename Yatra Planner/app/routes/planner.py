from fastapi import APIRouter

router = APIRouter(
    prefix='/plan',
    tags=['Travel Plan']
)

@router.post('/')
async def create_travel_plan():
    '''
    Aggregate weather, Currency and place data into single travel plan
    '''

    return {
        'message' : 'Travel plan created successfully'
    }