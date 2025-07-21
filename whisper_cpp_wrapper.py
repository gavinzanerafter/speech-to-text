import subprocess
import time
import os

class WhisperCPP:
    def __init__(self, binary=None, model=None):
        here = os.path.dirname(os.path.abspath(__file__))

        if binary is None:
            binary = os.path.join(here, "whisper.cpp", "build", "bin", "whisper-cli")
        if model is None:
            model = os.path.join(here, "whisper.cpp", "models", "ggml-small.en.bin")

        if not os.path.isfile(binary):
            raise FileNotFoundError(f"whisper.cpp binary not found at {binary}")
        if not os.path.isfile(model):
            raise FileNotFoundError(f"Model not found at {model}")

        self.binary = binary
        self.model = model

    def transcribe(self, audio_path: str, lang: str = "en") -> str:
        if not os.path.isfile(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        cmd = [
            self.binary,
            "-m", self.model,
            "-l", lang,
            "-nt",                # no timestamps
            "-f", audio_path
        ]
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time

        if result.returncode != 0:
            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            raise RuntimeError(f"whisper.cpp failed with exit code {result.returncode}")


        output_text = result.stdout.strip()
        return output_text, elapsed
