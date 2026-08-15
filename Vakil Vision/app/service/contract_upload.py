from fastapi import UploadFile, File, HTTPException
from uuid import uuid4
import os
from app.config import UPLOAD_DIR, ALLOWED_EXTENSION, MAX_SIZE_MB
from app.service.extract_content import extract_content


async def upload_file(file: UploadFile = File(...)):
    '''
    Upload the file
    '''
    # Get Extension
    ext = file.filename.split('.')[-1].lower()

    # Check the file is correct
    if ext not in ALLOWED_EXTENSION:
        raise HTTPException(status_code=404, detail='The file uploaded is of wrong type. (PDF or TXT required)')

    # Check for the size
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > MAX_SIZE_MB:
        raise HTTPException(status_code=413, detail='The file size uploaded in very large')

    # Create a local file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f'{uuid4()}.{ext}'
    path = os.path.join(UPLOAD_DIR, unique_filename)

    # Write to the file
    with open(path, 'wb') as f:
        f.write(content)

    data = await extract_content(path, ext)

    return {
        'filename' : unique_filename,
        'filetype' : ext,
        'raw_text' : data
    }