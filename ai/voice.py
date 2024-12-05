import whisper

model = whisper.load_model("small")

def transcribe(audio_path):
    if not audio_path:
        raise ValueError("Audio path must be provided")
    try:
        result = model.transcribe(audio_path, language="ru")
        return result.get("text", "")
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return ""
