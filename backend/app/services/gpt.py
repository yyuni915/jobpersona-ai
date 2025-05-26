# backend/app/services/gpt.py
import os
from dotenv import load_dotenv
import json
from openai import OpenAI
from models.interview_prep import InterviewPrep


load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_interview_prep_from_jd_resume(jd_text: str, resume_text: str) -> dict:
    prompt = f"""
                You are an expert interview analyst AI.

                You will be given:
                - A job description (JD)
                - A resume

                Your task is to:
                1. Extract the `industry` and `position` from the JD.
                2. Identify a list of all soft traits the JD implies.
                3. Choose the 5 most important soft traits.
                4. Extract all job skills mentioned in the JD.
                5. Choose the top 5 most important job skills.
                6. Analyze whether the resume's soft traits and job skills align with the JD or not.
                7. Write feedback that includes:
                - Match/mismatch of soft traits
                - Match/mismatch of job skills
                - Whether the resume is suitable or needs improvement
                - What to emphasize or be careful of during interview
                8. Generate the first interview question based on the JD.

                Respond in `InterviewPrep` format.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}
    """

    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are an expert job assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format=InterviewPrep
    )
    raw = response.choices[0].message.content

    # Try parsing it as JSON
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("GPT returned invalid JSON.")
