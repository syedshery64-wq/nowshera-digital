import os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Nowshera Digital ATS Backend API",
    description="Python FastAPI backend for Applicant Tracking System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STAGES_ORDER = ["Applied", "Shortlisted", "Interview", "Offer", "Hired"]

class JobCreate(BaseModel):
    title: str
    department: str
    location: str
    job_type: str
    openings: int
    deadline: str
    requirements: List[str]
    status: str = "Draft"

class StageUpdate(BaseModel):
    application_id: str
    recruiter_id: str
    next_stage: str

class ScheduleInterview(BaseModel):
    application_id: str
    recruiter_id: str
    interview_date: str
    interview_time: str
    location_or_link: str

db_jobs = {}
db_applications = {}
db_interviews = []

@app.post("/api/applications/apply")
async def apply_for_job(
    job_id: str = Form(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(...),
    candidate_phone: str = Form(...),
    cv_file: UploadFile = File(...)
):
    if not cv_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sirf PDF format ki CV accept hoti hai.")
    
    contents = await cv_file.read()
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="CV ka size 2MB se kam hona chahiye.")

    for app_id, app_data in db_applications.items():
        if app_data["candidate_email"] == candidate_email and app_data["job_id"] == job_id and app_data["stage"] != "Withdrawn":
            raise HTTPException(status_code=400, detail="Aap pehle hi is job ke liye apply kar chuke hain.")

    app_id = f"APP-{len(db_applications) + 1:03d}"
    new_application = {
        "id": app_id,
        "job_id": job_id,
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "candidate_phone": candidate_phone,
        "stage": "Applied",
        "created_at": datetime.now().isoformat(),
        "cv_filename": cv_file.filename,
        "ai_summary": None
    }
    
    db_applications[app_id] = new_application

    n8n_url = os.getenv("N8N_WEBHOOK_URL", "https://python7878.app.n8n.cloud/webhook-test/candidate-application")
    try:
        response = requests.post(
            n8n_url,
            json={
                "applicationId": app_id,
                "candidateName": candidate_name,
                "candidateEmail": candidate_email,
                "jobId": job_id,
                "cvText": "Candidate CV extracted content..."
            },
            timeout=5
        )
        if response.status_code == 200:
            new_application["ai_summary"] = response.json().get("aiSummary")
    except Exception:
        new_application["ai_summary"] = None

    return {
        "status": "success",
        "message": "Application kamyabi se receive ho gayi hai.",
        "application": new_application
    }

@app.post("/api/applications/change-stage")
def change_stage(data: StageUpdate):
    if data.application_id not in db_applications:
        raise HTTPException(status_code=404, detail="Application nahi mili.")

    app_data = db_applications[data.application_id]
    current_stage = app_data["stage"]

    if current_stage in ["Hired", "Rejected", "Withdrawn"]:
        raise HTTPException(status_code=400, detail="Closed application ka stage change nahi ho sakta.")

    if data.next_stage == "Rejected":
        app_data["stage"] = "Rejected"
        return {"status": "success", "new_stage": "Rejected"}

    try:
        curr_idx = STAGES_ORDER.index(current_stage)
        next_idx = STAGES_ORDER.index(data.next_stage)

        if next_idx != curr_idx + 1:
            raise HTTPException(
                status_code=400,
                detail=f"Aap stages skip nahi kar sakte. Agla step '{STAGES_ORDER[curr_idx + 1]}' hona chahiye."
            )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid stage.")

    app_data["stage"] = data.next_stage
    return {"status": "success", "new_stage": data.next_stage}

@app.post("/api/interviews/schedule")
def schedule_interview(data: ScheduleInterview):
    try:
        interview_dt = datetime.strptime(f"{data.interview_date} {data.interview_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Ghalat Date ya Time format.")

    if interview_dt < datetime.now():
        raise HTTPException(status_code=400, detail="Interview ka waqt future mein hona chahiye.")

    new_end_time = interview_dt + timedelta(hours=1)

    for inv in db_interviews:
        if inv["recruiter_id"] == data.recruiter_id:
            existing_start = datetime.strptime(f"{inv['date']} {inv['time']}", "%Y-%m-%d %H:%M")
            existing_end = existing_start + timedelta(hours=1)

            if max(interview_dt, existing_start) < min(new_end_time, existing_end):
                raise HTTPException(
                    status_code=400,
                    detail="Is recruiter ka pehle se is time par doosra interview scheduled hai."
                )

    new_interview = {
        "application_id": data.application_id,
        "recruiter_id": data.recruiter_id,
        "date": data.interview_date,
        "time": data.interview_time,
        "link": data.location_or_link
    }
    db_interviews.append(new_interview)

    if data.application_id in db_applications:
        db_applications[data.application_id]["stage"] = "Interview"

    return {"status": "success", "message": "Interview schedule ho gaya hai.", "interview": new_interview}

@app.post("/api/jobs/create")
def create_job(job: JobCreate):
    job_id = f"JOB-{len(db_jobs) + 1:03d}"
    db_jobs[job_id] = {**job.dict(), "id": job_id}
    return {"status": "success", "job": db_jobs[job_id]}

@app.get("/api/jobs")
def get_jobs(role: str = "Candidate"):
    if role == "Candidate":
        return [job for job in db_jobs.values() if job["status"] == "Open"]
    return list(db_jobs.values())
