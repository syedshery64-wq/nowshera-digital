# Nowshera Digital - AI-Powered Applicant Tracking System (ATS) with WhatsApp Integration

A full-stack, enterprise-grade Applicant Tracking System built for **Nowshera Digital** to solve hiring disorganization, lost CVs, interview collisions, slow candidate evaluations, and automated WhatsApp HR candidate communications.

---

## 🚀 Live Demo & Stack

- **Frontend**: Responsive Single-Page Application (HTML5, Tailwind CSS, JavaScript ES6+)
- **Backend API**: Python (FastAPI) + Pydantic + Uvicorn + WhatsApp Notification Service
- **Database**: Supabase PostgreSQL + Row Level Security (RLS) Policies
- **Automation Engine**: n8n Webhook Workflow (`python7878.app.n8n.cloud`)
- **Messaging**: WhatsApp API / Direct Click-to-Chat (`+92 316 1236343`)
- **AI Integration**: Google Gemini 1.5 Flash API (3-Part Structured CV Summarizer)

---

## ✨ Core Features & Roles

### 1. WhatsApp Automated Candidate Alerts & HR Chat
- Direct WhatsApp Support button (`+92 316 1236343`) in Candidate & Recruiter headers.
- Automatic WhatsApp payload trigger upon CV submission via n8n.
- One-click WhatsApp candidate messaging button for Recruiters.

### 2. Candidate Portal
- Browse open jobs (Draft jobs hidden automatically).
- PDF CV Upload Validator (Strict `.pdf` format check, max size 2MB).
- Single active application guard (Prevents duplicate applications).
- Application Tracking & Single-Click Withdrawal.

### 3. Recruiter Workspace
- Assigned job filter (Strict role-based viewing).
- **Gemini AI 3-Part CV Summary**:
  1. Short Profile (3–5 bullet points)
  2. Matched & Missing Job Requirements
  3. 3 Tailored Interview Questions
- **Anti-Bias Engine**: Strips age, gender, religion, marital status, and ignores prompt injections.
- **Strict Pipeline Enforcement**: `Applied` → `Shortlisted` → `Interview` → `Offer` → `Hired`.
- **Collision-Free Interview Scheduler**: Prevents past dates and 1-hour recruiter slot overlaps.

### 4. Admin / Hiring Manager Dashboard
- Real-time pipeline analytics, conversion funnels, and fill rates.
- Job posting lifecycle management (`Draft`, `Open`, `Closed`).
- Automated job closure upon reaching filled opening capacity.

---

## 🛠️ How to Run Locally

### 1. Run Python Backend
```bash
pip install fastapi uvicorn requests python-multipart pydantic
uvicorn main:app --reload --port 8000
```

### 2. Run Frontend
Open `index.html` directly in any web browser.
