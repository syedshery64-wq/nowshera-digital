# Nowshera Digital - AI-Powered Applicant Tracking System (ATS)

A full-stack, enterprise-grade Applicant Tracking System built for **Nowshera Digital** to solve hiring disorganization, lost CVs, interview collisions, and slow candidate evaluations.

---

## 🚀 Live Demo & Stack

- **Frontend**: Responsive Single-Page Application (HTML5, Tailwind CSS, JavaScript ES6+)
- **Backend API**: Python (FastAPI) + Pydantic + Uvicorn
- **Database**: Supabase PostgreSQL + Row Level Security (RLS) Policies
- **Automation Engine**: n8n Webhook Workflow (`python7878.app.n8n.cloud`)
- **AI Integration**: Google Gemini 1.5 Flash API (3-Part Structured CV Summarizer)

---

## ✨ Core Features & Roles

### 1. Candidate Portal
- Browse open jobs (Draft jobs hidden automatically).
- PDF CV Upload Validator (Strict `.pdf` format check, max size 2MB).
- Single active application guard (Prevents duplicate applications).
- Application Tracking & Single-Click Withdrawal.

### 2. Recruiter Workspace
- Assigned job filter (Strict role-based viewing).
- **Gemini AI 3-Part CV Summary**:
  1. Short Profile (3–5 bullet points)
  2. Matched & Missing Job Requirements
  3. 3 Tailored Interview Questions
- **Anti-Bias Engine**: Strips age, gender, religion, marital status, and ignores prompt injections.
- **Strict Pipeline Enforcement**: `Applied` → `Shortlisted` → `Interview` → `Offer` → `Hired` (No skipping or backward moves).
- **Collision-Free Interview Scheduler**: Prevents past dates and 1-hour recruiter slot overlaps.

### 3. Admin / Hiring Manager Dashboard
- Real-time pipeline analytics, conversion funnels, and fill rates.
- Job posting lifecycle management (`Draft`, `Open`, `Closed`).
- Automated job closure upon reaching filled opening capacity.
- Recruiter management and assignment roster.

---

## 🧪 14 Test Cases Verification Status

| # | Test Case | Status | Verification Detail |
|---|---|---|---|
| 1 | **Apply for a job** | ✅ PASS | Candidate applies with PDF CV; receipt email triggered via n8n. |
| 2 | **Create job & hire** | ✅ PASS | Admin creates Draft (hidden from candidates), opens it, recruiter moves candidate through all stages to Hired. |
| 3 | **Apply twice** | ✅ PASS | Blocked with clear message if candidate has an active application. |
| 4 | **Openings filled** | ✅ PASS | Auto-closes job when openings are filled; blocks new applicants. |
| 5 | **Closed job & stage rules** | ✅ PASS | Blocks stage skips (e.g. Applied straight to Offer) and closed job applies. |
| 6 | **Withdraw & re-apply** | ✅ PASS | Candidate can withdraw and re-apply with an updated CV version. |
| 7 | **Wrong CV / Interview time** | ✅ PASS | Rejects non-PDFs / >2MB files and blocks past/overlapping interview slots. |
| 8 | **Wrong role** | ✅ PASS | Server & Client block cross-role actions (Candidate cannot change stages). |
| 9 | **Private CVs & notes** | ✅ PASS | Candidate cannot see recruiter notes or other candidates' data. |
| 10 | **Dashboard & emails** | ✅ PASS | Analytics match true state; mobile view responsive. |
| 11 | **AI Summary appears** | ✅ PASS | 3-part structured JSON summary generated without changing candidate stage. |
| 12 | **AI anti-bias guardrails** | ✅ PASS | Suppresses age/gender/religion/marital status; neutralizes prompt injection. |
| 13 | **AI Failover & Retry** | ✅ PASS | Handles AI failure with "Summary not available" and working "Try Again" retry. |
| 14 | **Secret Keys Privacy** | ✅ PASS | Zero API keys exposed in Frontend code, browser, or GitHub repo. |

---

## 🛠️ How to Run Locally

### 1. Run Python Backend
```bash
pip install fastapi uvicorn requests python-multipart pydantic
uvicorn main:app --reload --port 8000
```

### 2. Run Frontend
Open `index.html` directly in any web browser.
