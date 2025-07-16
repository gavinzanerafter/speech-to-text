from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch

class TranscriptionModel:
    def __init__(self, model_name="openai/whisper-small"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name).to(self.device)

    def transcribe(self, audio_or_path, sr=16000):
        if isinstance(audio_or_path, str):
            import librosa
            speech, sr = librosa.load(audio_or_path, sr=sr)
        else:
            speech = audio_or_path

        input_features = self.processor(speech, sampling_rate=sr, return_tensors="pt").input_features.to(self.device)
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
