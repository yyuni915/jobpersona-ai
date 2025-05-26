# backend/app/routes/analyse.py

from fastapi import APIRouter, UploadFile, File, Form, Depends
from utils.auth import verify_google_token
from utils.file import extract_text_from_pdf
from services.gpt import generate_interview_prep_from_jd_resume
from services.gemini import gemini_analyse 
from models.interview_prep import InterviewPrep
from models.interview_response import InterviewResponse
from models.interview_request import InterviewRequest
import json

router = APIRouter(prefix="/interview", tags=["interview"])


@router.post("/setup", response_model=InterviewPrep)
async def prepare_interview(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),  
    user_id: str = "test-user-123"
    # user_id: str = Depends(verify_google_token)
):

    resume_text = extract_text_from_pdf(resume)

    try:
        prep_data = generate_interview_prep_from_jd_resume(jd_text, resume_text)

    except Exception as e:
        return {
            "error": "Keyword extraction failed",
            "reason": str(e)
        }

    return prep_data  

@router.post("/analysis", response_model=InterviewResponse)
async def analyse_interview(
    file: UploadFile = File(...),
    data: str = Form(...),  
    user_id: str = "test-user-123"
    # user_id: str = Depends(verify_google_token)
):
    
    parsed_data = json.loads(data)
    interview_data  = InterviewRequest(**parsed_data)  

    result = gemini_analyse(file, interview_data)  
    return result
