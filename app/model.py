from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import torchaudio
import librosa

class TranscriptionModel:
    def __init__(self, model_name="openai/whisper-small"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name).to(self.device)

    def transcribe(self, audio_path):
        # load & preprocess audio
        speech, sr = librosa.load(audio_path, sr=16000)
        input_features = self.processor(speech, sampling_rate=16000, return_tensors="pt").input_features.to(self.device)

        # generate tokens
        predicted_ids = self.model.generate(input_features)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
