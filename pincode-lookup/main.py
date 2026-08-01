from fastapi import FastAPI
from exception import (
    PincodeNotFoundError,
    InvalidPincodeError,
    invlaid_pincode_handler,
    pincode_not_found_handler
)
from data import pincode_db
from model import BulkResponse, LocationResponse, BulkRequest

app = FastAPI(
    title= 'Pincode lookup AI',
    description= 'Fetch city and State from pincode'
)

# Register custom exceptions created
app.add_exception_handler(PincodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError, invlaid_pincode_handler)

@app.get('/')
def root():
    return {'message' : 'Welcome to Pincode Lookup'}

@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code : str):
    if len(code) != 6 or not code.isdigit():
        raise InvalidPincodeError(code, "Pincode enetered is not valid")
    if code not in pincode_db:
        raise PincodeNotFoundError(code)
    return pincode_db[code]

@app.post("/pincode/bulk", response_model=BulkResponse)
def lookup_bulk(request: BulkRequest):
    results = []
    missed = []

    for code in request.pincodes:
        if code in pincode_db:
            results.append(pincode_db[code])
        else:
            missed.append(code)

    return BulkResponse(
            found = len(results),
            not_found=len(missed),
            result = results,
            missing = missed
        )