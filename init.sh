#!/bin/bash
echo "Downloading Whisper model and processor..."
python3 -c "
from transformers import WhisperProcessor, WhisperForConditionalGeneration
WhisperProcessor.from_pretrained('openai/whisper-small')
WhisperForConditionalGeneration.from_pretrained('openai/whisper-small')
"
echo "Done. Models cached in ~/.cache/huggingface/"
