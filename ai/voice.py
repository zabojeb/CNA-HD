import whisper

model = whisper.load_model("large")
result = model.transcribe("test_audio.mp3")

print(result["text"])