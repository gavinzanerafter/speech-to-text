from fastapi import FastAPI, UploadFile
from app.model import TranscriptionModel
from app.chunk import chunk_audio
import shutil
import os
import librosa

app = FastAPI()
model = TranscriptionModel()

@app.post("/transcribe/")
async def transcribe(file: UploadFile):
    tmp_path = f"data/{file.filename}"
    with open(tmp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # load audio
    speech, sr = librosa.load(tmp_path, sr=16000)

    # chunk it
    chunks = chunk_audio(speech, sr, chunk_duration=30, overlap=2)

    # transcribe each chunk
    transcript = ""
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}/{len(chunks)}...")
        text = model.transcribe(chunk, sr)
        transcript += text + " "

    # os.remove(tmp_path)
    return {"transcription": transcript.strip()}
