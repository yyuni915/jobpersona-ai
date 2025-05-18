from pydantic import BaseModel

class InterviewFeedback(BaseModel):
    transcript: str
    confidence: str
    tone: str
    clarity_score: float
    gemini_summary: str