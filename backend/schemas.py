from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import ApplicationStatus

# ── USER SCHEMAS ──────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime

    class Config:
        from_attributes = True

# ── AUTH SCHEMAS ──────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ── ANALYSIS SCHEMAS ──────────────────────────────────────

class AnalysisOut(BaseModel):
    fit_score: Optional[float]
    matched_keywords: Optional[str]
    missing_keywords: Optional[str]
    extracted_skills: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ── APPLICATION SCHEMAS ───────────────────────────────────

class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: ApplicationStatus = ApplicationStatus.APPLIED
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None

class ApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str
    job_url: Optional[str]
    notes: Optional[str]
    applied_date: Optional[datetime]
    follow_up_date: Optional[datetime]
    created_at: datetime
    analysis: Optional[AnalysisOut] = None

    class Config:
        from_attributes = True

# ── ANALYTICS SCHEMAS ─────────────────────────────────────

class ApplicationStats(BaseModel):
    total: int
    applied: int
    interview: int
    offer: int
    rejected: int
    withdrawn: int
    interview_rate: float   # interviews / total
    offer_rate: float       # offers / total