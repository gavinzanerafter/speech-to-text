from whisper_cpp_wrapper import WhisperCPP
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="Path to audio file (WAV, 16kHz mono preferred)")
    args = parser.parse_args()

    whisper = WhisperCPP()
    print(f"Transcribing {args.audio} ...")
    text, elapsed = whisper.transcribe(args.audio)
    print(f"\n--- Transcription ---\n{text}\n")
    print(f"Elapsed time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
