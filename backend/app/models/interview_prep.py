# backend/app/models/keyword_analysis.py

from pydantic import BaseModel
from typing import List

class InterviewPrep(BaseModel):
    industry: List[str]
    position: str
    jd_soft_traits_list: List[str]
    jd_soft_traits_top5: List[str]
    jd_job_skills_list: List[str]
    jd_job_skills_top5: List[str]
    feedback: str  
    questions: List[str]