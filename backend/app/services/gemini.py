import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import UploadFile
import tempfile

load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")


genai.configure(api_key=api_key)

def gemini_analyse(file: UploadFile, session):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        contents = file.file.read()
        temp_video.write(contents)
        temp_video_path = temp_video.name

    client = genai.Client()

    uploaded_file = client.files.upload(file=temp_video_path)

    prompt = """
    This is a job interview video. First, summarize the speaker's overall communication style, tone, and personality traits.

    Then:
    1. Give feedback on how well the answer follows the STAR format.
    2. Suggest 1 follow-up interview questions that would test this candidate’s depth in the topic.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",  
        contents=[uploaded_file, prompt]
    )

    return {
        "gemini_feedback": response.text
    }
