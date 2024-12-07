import os
import shutil

import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette import status

app = FastAPI(docs_url="/docs")

UPLOAD_DIR = "./images"
MAX_FILE_SIZE = 1.5 * 1024 * 1024
ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]


@app.post("/image/upload/")
async def upload_image(file: UploadFile = File(..., description="upload any file")):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="file is too large")
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Unknown file type")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"file uploaded to {UPLOAD_DIR}"}


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", reload=True)
