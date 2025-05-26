import os
import shutil
from dotenv import load_dotenv
from google import genai
from fastapi import UploadFile
import tempfile
from models.interview_response import InterviewResponse, SoftTraitEvaluation
from models.interview_request import InterviewRequest
from utils.transcription import transcribe_video_with_whisper
import json

load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

def gemini_analyse(file: UploadFile, interview_data: InterviewRequest) -> InterviewResponse:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        shutil.copyfileobj(file.file, temp_video)
        temp_video_path = temp_video.name

    video = client.files.upload(file=temp_video_path)
    
    # STEP 1: Transcribe video
    answer_text = transcribe_video_with_whisper(temp_video_path)

    # Prompt for analysis
    prompt = f"""
    You are analysing a job interview answer from a candidate applying for a {interview_data.position} role in {interview_data.industry}.
    The interview question was: "{interview_data.question}"
    
    1. Non-Verbal Soft Trait Evaluation (video/audio only)
    IMPORTANT: You are NOT allowed to consider what the candidate said. Do not base your answers on content or accomplishments.

    Only evaluate personality traits based on:
    - Voice tone
    - Facial expressions
    - Posture
    - Eye contact
    - General vibe or emotional impression

    For example:
    - A calm tone and relaxed posture = calmness
    - A warm smile and gentle tone = empathy
    - Loud volume and confident eye contact = assertiveness
 
    For each trait below, say whether it was demonstrated (true/false) and explain why — based on only what is visible/audible from the video.  
    You are NOT evaluating what they said, only how they expressed themselves.
    
    Traits to evaluate:
    {', '.join(interview_data.jd_soft_traits_nonverbal)}

    For each of the following soft traits, answer whether they were demonstrated (true/false), and provide a short reason:
    Traits: {', '.join(interview_data.jd_soft_traits_nonverbal_top5)}
    - In 1–2 sentences, summarize the candidate’s non-verbal impression:  
    (e.g., “They appeared nervous and avoided eye contact” or “Confident and relaxed body posture”)
    
    (Optional) Personality Typing:

    Based only on non-verbal impression, which MBTI type or Big Five traits might this candidate reflect?
    Give 1–2 sentence justification (e.g., “likely Introverted due to low eye contact and soft voice”).

    This is speculative — accuracy is not expected.


    2. Structure & Content Quality (based on transcribed text)
    
    Transcribed Answer:
    \"\"\"{answer_text}\"\"\"

    - Did the candidate use STAR structure? (true/false + short reason)
    - Was the answer relevant to the question? (true/false + short reason)
    - Was the answer clear and focused? (true/false + short reason)


    3. Technical Evaluation (if this was a technical question)

    If the question is technical, evaluate the following:

    - Use the following as possible technical keywords to expect: {', '.join(interview_data.jd_job_skills_list)}
    - Based on the interview question, determine which of these are relevant and expected.
    - Actual keywords found in the answer
    - Was the technical explanation insightful? (true/false + brutally honest feedback + what could be improved)
    - Was the technical depth strong? (shallow / clear / detailed / deep_dive) + brutally honest feedback
    
    
    4. Long-form Personality Description (non-verbal only)

    You are a behavioral profiler observing the candidate’s non-verbal cues only — tone of voice, facial expressions, posture, gestures, eye contact, rhythm, and energy.
    Do NOT analyze or refer to anything they said.
    Write a long-form psychological and behavioral analysis describing what type of person they appear to be — as if you were writing a dossier on them. This is not about the interview answer. This is about who they are as a human based on how they physically present themselves.

    You must include:
    - Estimated **age range**
    - Likely **background or lifestyle** (e.g., “seems to have a structured, disciplined work history” or “feels creative but scattered”)
    - Emotional temperament (e.g., “calm but slightly performative,” “suppressed anxiety under confident tone”)
    - Confidence level and how it's expressed
    - How they **carry themselves** — e.g., “rehearsed,” “natural,” “guarded,” “disconnected,” “authentic”
    - Personality contradictions, if any
    - General impression: Would others trust this person? Follow them? Avoid them?
    - Describe how expressive or withdrawn they are, how they navigate discomfort, and whether they seem sincere
    - Speculative MBTI type
        
    Then close with:
    **"Based on non-verbal presence alone, they may align with [MBTI type(s)]."**

    Be extremely descriptive. At least **5–8 sentences** minimum. Do not summarize. Write like you're watching a subject in a documentary and describing them in a field journal.
    
    """   
    

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[video, prompt],
        config={
        "response_mime_type": "application/json",
        "response_schema": InterviewResponse,
        }
    )

    try:
        return InterviewResponse(**json.loads(response.text))
    except Exception as e:
        print("Could not manually parse Gemini output either.")
        print(e)
        raise ValueError("Gemini output is invalid.")    
        # Print raw JSON
        print("Raw JSON output:\n", response.text)

