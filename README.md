# 🎙️ Speech-to-Text with whisper.cpp

This project is a fast, **offline speech-to-text system** using [whisper.cpp](https://github.com/ggerganov/whisper.cpp) with a Python wrapper and benchmarking script.

It is designed to transcribe audio locally, securely, and quickly — suitable for sensitive interviews, live news, or other low-latency use cases.

---

## 🚀 Features
✅ Offline transcription — no cloud required  
✅ Uses `ggml-tiny-q5_1.bin` quantized model for high speed & small size  
✅ Runs on macOS, Linux, Windows (CPU)  
✅ Written in Python + C++

---

## 📋 Requirements

- **CMake ≥ 3.15**
  - Install via Homebrew (macOS):
    ```bash
    brew install cmake
    ```
  - Or via apt (Linux):
    ```bash
    sudo apt install cmake
    ```
  - Or download from [https://cmake.org](https://cmake.org).

- Python 3.8+
  - Install dependencies (optional for Python parts):
    ```bash
    pip install -r requirements.txt
    ```

---

## 📁 Folder Structure

````

speech-to-text/
├── benchmark.py               # Python benchmark script
├── whisper\_cpp\_wrapper.py     # Python wrapper for whisper.cpp
├── whisper.cpp/               # whisper.cpp source code
│   ├── CMakeLists.txt
│   ├── build/                 # (ignored) build artifacts
│   ├── models/                # (ignored) model weights
│   ├── …
├── .gitignore
├── README.md

````

---

## 🔧 Setup

1️⃣ Clone this repository:
```bash
git clone https://github.com/yourname/speech-to-text.git
cd speech-to-text
````

2️⃣ Build `whisper.cpp`:

```bash
cd whisper.cpp
make
```

This creates the binary at:

```
whisper.cpp/build/bin/whisper-cli
```

3️⃣ Download the model:
We recommend the `tiny-q5_1` quantized English model for fastest performance:

```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh tiny.en.q5_1
```

This downloads to:

```
whisper.cpp/models/ggml-tiny.en.q5_1.bin
```

---

## 🎤 Audio Requirements

Input audio **must** be:

* `.wav` format
* mono
* 16 kHz sample rate

To convert:

```bash
ffmpeg -i input.wav -ar 16000 -ac 1 output_16k.wav
```

---

## 🏃 Run

### From Python:

```bash
cd /path/to/speech-to-text
python3 benchmark.py ~/Desktop/example_16k.wav
```

You should see output similar to:

```
Transcribing ~/Desktop/example_16k.wav ...

--- Transcription ---
hello world this is a test

Elapsed time: 0.9 seconds
```

---

### Directly via whisper.cpp:

```bash
cd whisper.cpp
./build/bin/whisper-cli \
  -m models/ggml-tiny.en.q5_1.bin \
  -f ~/Desktop/example_16k.wav \
  -nt
```

---

## 📌 Notes

* Do **NOT** commit `models/` or `build/` to Git — they are large and machine-specific.
* `.gitignore` already excludes these.

---

## 📚 References

* [whisper.cpp](https://github.com/ggerganov/whisper.cpp) — the underlying engine
* [OpenAI Whisper paper](https://arxiv.org/abs/2212.04356)

---

## 🔮 Future Work

✅ Real-time streaming with WebSockets
✅ React.js + TailwindCSS frontend
✅ Automatic model download & setup

---

Enjoy!
