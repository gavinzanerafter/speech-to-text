import librosa
import numpy as np

def chunk_audio(audio, sr, chunk_duration=30, overlap=2):
    chunk_samples = int(chunk_duration * sr)
    overlap_samples = int(overlap * sr)
    chunks = []
    for start in range(0, len(audio), chunk_samples - overlap_samples):
        end = min(start + chunk_samples, len(audio))
        chunks.append(audio[start:end])
        if end == len(audio):
            break
    return chunks
