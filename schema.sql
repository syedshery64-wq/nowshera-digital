-- Supabase PostgreSQL Schema for Nowshera Digital ATS Project wvfcxcxxfajkupzpvvsi

-- 1. Profiles Table
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  role TEXT CHECK (role IN ('Candidate', 'Recruiter', 'Admin')) NOT NULL DEFAULT 'Candidate',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Jobs Table
CREATE TABLE IF NOT EXISTS public.jobs (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  department TEXT NOT NULL,
  location TEXT NOT NULL,
  job_type TEXT NOT NULL,
  openings INT NOT NULL DEFAULT 1,
  deadline DATE NOT NULL,
  requirements JSONB NOT NULL,
  status TEXT CHECK (status IN ('Draft', 'Open', 'Closed')) DEFAULT 'Draft',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Recruiter Assignments
CREATE TABLE IF NOT EXISTS public.recruiter_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id TEXT REFERENCES public.jobs(id) ON DELETE CASCADE,
  recruiter_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  assigned_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Applications Table
CREATE TABLE IF NOT EXISTS public.applications (
  id TEXT PRIMARY KEY,
  job_id TEXT REFERENCES public.jobs(id) ON DELETE CASCADE,
  candidate_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  candidate_name TEXT NOT NULL,
  candidate_email TEXT NOT NULL,
  stage TEXT CHECK (stage IN ('Applied', 'Shortlisted', 'Interview', 'Offer', 'Hired', 'Rejected', 'Withdrawn')) DEFAULT 'Applied',
  cv_url TEXT NOT NULL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. AI Summaries Table
CREATE TABLE IF NOT EXISTS public.ai_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id TEXT REFERENCES public.applications(id) ON DELETE CASCADE,
  short_profile JSONB NOT NULL,
  matched_requirements JSONB NOT NULL,
  missing_requirements JSONB NOT NULL,
  interview_questions JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Interviews Table
CREATE TABLE IF NOT EXISTS public.interviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id TEXT REFERENCES public.applications(id) ON DELETE CASCADE,
  recruiter_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
  interview_date DATE NOT NULL,
  interview_time TIME NOT NULL,
  meeting_link TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row Level Security (RLS) Policies
ALTER TABLE public.applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_summaries ENABLE ROW LEVEL SECURITY;

-- Candidates can only view their own applications
CREATE POLICY candidate_read_own_applications ON public.applications
  FOR SELECT USING (auth.uid() = candidate_id);

-- Candidates CANNOT view AI summaries or recruiter notes
CREATE POLICY block_candidate_ai_summaries ON public.ai_summaries
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM public.profiles 
      WHERE profiles.id = auth.uid() AND profiles.role IN ('Recruiter', 'Admin')
    )
  );
