import os
from uuid import uuid4

from fastapi import UploadFile


os.makedirs("images", exist_ok=True)


async def upload_image(file: UploadFile) -> str:
    file_extension = os.path.splitext(file.filename)[1]

    unique_filename = f"{uuid4()}{file_extension}"

    file_location = os.path.join(
        "images",
        unique_filename
    )

    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_location