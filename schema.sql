-- Supabase PostgreSQL Schema with WhatsApp Contact Fields
CREATE TABLE IF NOT EXISTS public.applications (
  id TEXT PRIMARY KEY,
  job_id TEXT REFERENCES public.jobs(id) ON DELETE CASCADE,
  candidate_name TEXT NOT NULL,
  candidate_email TEXT NOT NULL,
  candidate_phone TEXT DEFAULT '03161236343',
  whatsapp_enabled BOOLEAN DEFAULT TRUE,
  stage TEXT CHECK (stage IN ('Applied', 'Shortlisted', 'Interview', 'Offer', 'Hired', 'Rejected', 'Withdrawn')) DEFAULT 'Applied',
  cv_url TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
