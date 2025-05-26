# backend/app/main.py

from fastapi import FastAPI
from routes import interview 

app = FastAPI()
app.include_router(interview.router)

@app.get("/")
def root():
    return {"message": "JobPersona backend is running"}

