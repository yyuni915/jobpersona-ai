import whisper

def transcribe_video_with_whisper(file_path: str) -> str:
    model = whisper.load_model("tiny")
    result = model.transcribe(file_path)
    return result["text"]