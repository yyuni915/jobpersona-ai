from pydantic import BaseModel
from typing import List

class InterviewRequest(BaseModel):
    question_index: int
    question: str
    industry: List[str]
    position: str
    jd_soft_traits_nonverbal_top5: List[str]
    jd_soft_traits_nonverbal: List[str]
    jd_job_skills_list: List[str]
    finished: bool

