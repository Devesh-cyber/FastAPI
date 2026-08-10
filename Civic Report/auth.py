from fastapi import Header, HTTPException

API_KEY = '123'

async def verify_api_key(api_key: str = Header()):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail='Invalid API KEY Entered')
    return api_key