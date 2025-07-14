from jiwer import wer

def calculate_wer(ref: str, hyp: str):
    return wer(ref, hyp)
