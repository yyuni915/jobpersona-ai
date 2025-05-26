from pydantic import BaseModel
from typing import List, Optional

class SoftTraitEvaluation(BaseModel):
    trait: str
    matched: bool
    reason: str

class InterviewResponse(BaseModel):
    question_index: int
    question: str
    is_technical: bool

    # 1. Persona — always present
    evaluated_soft_traits_nonverbal : List[SoftTraitEvaluation]

    # 2. Structure & Content Quality
    is_star_format: bool
    star_reason: str

    relevance: bool
    relevance_reason: str

    is_clear_and_focused: bool
    clarity_reason: str

    # 3. Technical Insight — only if technical question
    technical_expected_keywords: Optional[List[str]] = None  # internal use only
    technical_keywords_found: Optional[List[str]] = None     # GPT extracts this
    technical_insight: Optional[bool] = None
    technical_depth: Optional[str] = None

    # 4. Personality descriptio
    personality_description: Optional[str] = None

    # Always
    finished: bool