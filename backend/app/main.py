# backend/app/main.py

from fastapi import FastAPI
from routes import analyse 

app = FastAPI()
app.include_router(analyse.router)

@app.get("/")
def root():
    return {"message": "JobPersona backend is running"}

