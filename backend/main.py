from fastapi import FastAPI, WebSocket
import asyncio
import wave
import subprocess
import os

app = FastAPI()

# 16kHz mono, 16-bit PCM
SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
CHANNELS = 1
BUFFER_DURATION = 1.0  # seconds
BUFFER_SIZE = int(SAMPLE_RATE * SAMPLE_WIDTH * BUFFER_DURATION)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")

    buffer = bytearray()
    idx = 0

    try:
        while True:
            chunk = await websocket.receive_bytes()
            buffer.extend(chunk)

            if len(buffer) >= BUFFER_SIZE:
                # write to wav
                filename = f"temp_{idx}.wav"
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(SAMPLE_WIDTH)
                    wf.setframerate(SAMPLE_RATE)
                    wf.writeframes(buffer[:BUFFER_SIZE])

                # remove used buffer
                buffer = buffer[BUFFER_SIZE:]

                # run whisper.cpp
                result = subprocess.run(
                    [
                        "./whisper.cpp/build/bin/whisper-cli",
                        "-m", "models/ggml-tiny-q5_1.bin",
                        "-f", filename,
                        "-otxt",
                        "-of", f"out_{idx}"
                    ],
                    capture_output=True, text=True
                )

                print("whisper.cpp stdout:", result.stdout)
                print("whisper.cpp stderr:", result.stderr)

                # read transcript
                transcript_path = f"out_{idx}.txt"
                transcript = ""
                if os.path.exists(transcript_path):
                    with open(transcript_path, "r") as f:
                        transcript = f.read().strip()
                    os.remove(transcript_path)

                if transcript and transcript.strip() not in ("", "[BLANK_AUDIO]"):
                    await websocket.send_text(transcript)
                # else:
                #     await websocket.send_text("[no transcription]")

                os.remove(filename)
                idx += 1

    except Exception as e:
        print("WebSocket closed:", e)
    finally:
        await websocket.close()
