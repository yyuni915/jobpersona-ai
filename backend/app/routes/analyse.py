# backend/app/routes/analyse.py

from fastapi import APIRouter, UploadFile, File, Form, Depends
from utils.auth import verify_google_token
from services.file_utils import extract_text_from_pdf
from services.gpt import extract_keywords_from_jd_resume_gpt
from services.gemini import gemini_analyse 
from models.interview_prep import InterviewPrep

router = APIRouter(prefix="/analyse", tags=["Analyse"])


@router.post("/jd-resume", response_model=InterviewPrep)
async def upload_jd_resume_for_analysis(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),  
    user_id: str = "test-user-123"
    # user_id: str = Depends(verify_google_token)
):

    # 2. Resume PDF → text extract
    resume_text = extract_text_from_pdf(resume)

    # 3. GPT keyword extract
    try:
        keywords = extract_keywords_from_jd_resume_gpt(jd_text, resume_text)
        print(jd_text)
        print(resume_text)

    except Exception as e:
        return {
            "error": "Keyword extraction failed",
            "reason": str(e)
        }

    return keywords  

@router.post("/interview")
async def analyse_interview(
    file: UploadFile = File(...), 
    user_id: str = Depends(verify_google_token)
):
    # user_id → session_id or real user_id
    result = gemini_analyse(file.file)
    return result
