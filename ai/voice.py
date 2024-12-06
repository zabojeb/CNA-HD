import whisper
import torch

DEBUG = True
if DEBUG:
    model = whisper.load_model("tiny", device="cpu")
else:
    model = whisper.load_model("medium", device="cuda" or "cpu" if torch.cuda.is_available() else "cpu")

def transcribe(audio_path):
    if not audio_path:
        raise ValueError("Audio path must be provided")
    try:
        result = model.transcribe(audio_path, language="ru")
        return result.get("text", "")
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""
