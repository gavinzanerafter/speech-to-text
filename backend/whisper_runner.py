import subprocess
import tempfile
from pathlib import Path

WHISPER_BIN = Path("./whisper.cpp/build/bin/whisper-cli")
MODEL_PATH = Path("./models/ggml-tiny-q5_1.bin")

def transcribe(audio_bytes: bytes) -> str:
    # save the incoming blob
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_in:
        tmp_in.write(audio_bytes)
        tmp_in_path = tmp_in.name

    # convert to wav
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_out:
        tmp_out_path = tmp_out.name

    ffmpeg_cmd = [
        "ffmpeg", "-y", "-i", tmp_in_path,
        "-ar", "16000", "-ac", "1", "-f", "wav", tmp_out_path
    ]
    result_ffmpeg = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    Path(tmp_in_path).unlink()  # cleanup original

    if result_ffmpeg.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result_ffmpeg.stderr.decode()}")

    # now run whisper.cpp
    cmd = [
        str(WHISPER_BIN),
        "-m", str(MODEL_PATH),
        "-f", tmp_out_path,
        "-nt"
    ]

    cmd = [
        str(WHISPER_BIN),
        "-m", str(MODEL_PATH),
        "-f", tmp_out_path,
        "-nt"
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    print("=== whisper.cpp stdout ===")
    print(result.stdout)
    print("=== whisper.cpp stderr ===")
    print(result.stderr)
    print("=== whisper.cpp return code ===")
    print(result.returncode)

    Path(tmp_out_path).unlink()


    if result.returncode != 0:
        raise RuntimeError(f"whisper.cpp error: {result.stderr}")

    return result.stdout
