import aiofiles
from fastapi import FastAPI, UploadFile, HTTPException
from pathlib import Path

from . import settings


app = FastAPI()
app_settings = settings.get_settings()
upload_path = app_settings.data_path
upload_path.mkdir(exist_ok=True)


@app.post("/documents")
async def upload_document(file: UploadFile):
    if not file.filename or not file.size:
        raise HTTPException(status_code=400, detail="Malformed request or missing file")

    if file.size > app_settings.max_file_size:
        raise HTTPException(status_code=413, detail="File too large")

    file_path = Path(upload_path, file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(app_settings.chunk_size):
            await f.write(chunk)

    return {"filename": file_path.name, "size": file_path.stat().st_size}
