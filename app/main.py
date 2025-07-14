from fastapi import FastAPI, UploadFile
from app.model import TranscriptionModel
import shutil
import os

app = FastAPI()
model = TranscriptionModel()

@app.post("/transcribe/")
async def transcribe(file: UploadFile):
    tmp_path = f"data/{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"transcription": text}
