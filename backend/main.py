from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from fastapi.middleware.cors import CORSMiddleware

from services.ai_parser import (
    extract_text_from_pdf,
    extract_skills,
    calculate_match
)

from services.job_scraper import fetch_jobs

app = FastAPI()

# ======================================================
# CORS
# ======================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ======================================================
# HOME
# ======================================================

@app.get("/")
def home():

    return {
        "message": "HO Resume Screener API Running"
    }

# ======================================================
# ATS RESUME MATCH
# ======================================================

@app.post("/match-resume/")
async def match_resume(

    file: UploadFile = File(...),

    job_description: str = Form(...)

):

    # EXTRACT TEXT

    resume_text = extract_text_from_pdf(
        file.file
    )

    # EXTRACT SKILLS

    skills = extract_skills(
        resume_text
    )

    # ATS MATCH

    result = calculate_match(
        skills,
        job_description
    )

    return {

        "filename": file.filename,

        "skills": skills,

        "ats_result": result

    }

# ======================================================
# JOBS API
# ======================================================

@app.get("/jobs/{domain}/{state}")
def get_jobs(domain: str, state: str):

    try:

        jobs = fetch_jobs(
            domain,
            state
        )

        # SAFETY

        if not isinstance(jobs, list):

            return []

        return jobs

    except Exception as e:

        print("JOBS ERROR:", e)

        return []