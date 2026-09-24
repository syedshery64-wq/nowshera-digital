import os
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Nowshera Digital ATS Backend API",
    description="Python FastAPI backend for Applicant Tracking System with WhatsApp Notification Engine",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STAGES_ORDER = ["Applied", "Shortlisted", "Interview", "Offer", "Hired"]
OFFICIAL_WHATSAPP = "923161236343"

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

class WhatsAppAlert(BaseModel):
    phone_number: str
    message: str

db_jobs = {}
db_applications = {}
db_interviews = []

@app.post("/api/whatsapp/send-alert")
def send_whatsapp_alert(data: WhatsAppAlert):
    # Sends WhatsApp message payload to candidate or HR
    formatted_phone = data.phone_number.replace("+", "").replace(" ", "").replace("-", "")
    whatsapp_url = f"https://wa.me/{formatted_phone}?text={data.message}"
    
    return {
        "status": "success",
        "official_hr_whatsapp": OFFICIAL_WHATSAPP,
        "whatsapp_url": whatsapp_url,
        "message_sent": data.message
    }

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
        "ai_summary": None,
        "whatsapp_link": f"https://wa.me/{OFFICIAL_WHATSAPP}?text=Hello%20Nowshera%20Digital,%20I%20have%20applied%20for%20Application%20ID:%20{app_id}"
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
                "candidatePhone": candidate_phone,
                "hrWhatsApp": OFFICIAL_WHATSAPP,
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
