from app.config import GEMINI_API_KEY
from app.database import contracts_collection
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.service.gemini_analyze import analyze_contract

router = APIRouter(
    prefix='/analysis',
    tags=['Analysis']
)

@router.post('/analyse/{contract_id}')
async def analyse_contract(contract_id: str):

    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail='AI API Key is not configured')

    contract = contracts_collection.find_one({'_id' : ObjectId(contract_id)})

    if not contract:
        raise HTTPException(status_code=404, detail='Could not found')

    if not contract.get('text_content'):
        raise HTTPException(status_code=400, detail='Contract has no text content to analyze')

    contracts_collection.update_one({'_id' : ObjectId(contract_id)},{'$set' : {'analysis_status' : 'in_progress'}})

    result = await analyze_contract(contract_id, contract['text_content'])