# backend/app/models/keyword_analysis.py

from pydantic import BaseModel
from typing import List

class InterviewPrep(BaseModel):
    industry: List[str]
    position: str
    jd_soft_traits_nonverbal: List[str]
    jd_soft_traits_nonverbal_top5 : List[str]
    jd_job_skills_list: List[str]
    feedback: str  
    first_question: str