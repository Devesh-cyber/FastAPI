from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from app.config import ALLOWED_EXTENSIONS, UPLOAD_DIR, MAX_SIZE_IN_MB
from app.models import Contract
from app.service.document_parser import extract_text
from app.database import contracts_collection

router = APIRouter(
    prefix='/contracts',
    tags=['Contracts']
)


@router.post('/upload')
async def upload_contract(file: UploadFile = File(...)):

    # 1. Check file exist
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    # 2. Check file extension is valid
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail='Invalid file type. (only PDF and txt)')

    content = await file.read()

    # 3. Check file size
    size_mb = len(content) / (1024 * 1024)

    if size_mb > MAX_SIZE_IN_MB:
        raise HTTPException(status_code=404, detail='Max side of file to upload is 10MB')

    # 4. Save file in our local machine
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f'{uuid.uuid1()}{ext}'
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    with open(file_path, 'wb') as f:
        f.write(content)

    # 5. Extract the content from the document
    parser, page_count, word_count = extract_text(file_path)

    # 6. 
    contract_data =  Contract(
        filename=unique_filename,
        original_name=file.filename,
        text_content=parser,
        page_count=page_count,
        word_count=word_count,
    )

    # 7. Save data to db
    doc = contract_data.model_dump()
    result = contracts_collection.insert_one(doc)
    contract_id = str(result.inserted_id)

    return {
        'message' : 'File uploaded and precoessed successfully',
        'contract' : contract_data.model_dump(),
        'id' : contract_id
        }
    