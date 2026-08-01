from fastapi.responses import JSONResponse
from fastapi import Request

class PincodeNotFoundError(Exception):
    def __init__(self, pincode : str):
        self.pincode = pincode

class InvalidPincodeError(Exception):
    def __init__(self, pincode : str, reason : str):
        self.pincode = pincode
        self.reason = reason


async def pincode_not_found_handler(request : Request, exc : PincodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            'error' : 'pincode not found',
            'message' : f'No location for pincode {exc.pincode}',
            'pincode' : exc.pincode
        }
    )

async def invlaid_pincode_handler(request : Request, exc : InvalidPincodeError):
    return JSONResponse(
        status_code=400,
        content = {
            'error' : 'Invalid Pincode',
            'message' : f'Pincode {exc.pincode} invalid bcoz {exc.reason}',
            'pincode' : exc.pincode
        }
    )