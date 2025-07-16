import numpy as np

def chunk_audio(audio, sr, chunk_duration=30, overlap=2):
    """
    Splits audio into overlapping chunks.

    Args:
        audio (np.ndarray): 1D audio array
        sr (int): sample rate (Hz)
        chunk_duration (int): chunk length in seconds
        overlap (int): overlap between chunks in seconds

    Returns:
        List[np.ndarray]: list of audio chunks
    """
    chunk_samples = int(chunk_duration * sr)
    overlap_samples = int(overlap * sr)
    chunks = []
    for start in range(0, len(audio), chunk_samples - overlap_samples):
        end = min(start + chunk_samples, len(audio))
        chunks.append(audio[start:end])
        if end == len(audio):
            break
    return chunks
