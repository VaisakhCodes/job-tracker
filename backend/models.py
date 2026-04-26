from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # One user has many applications
    applications = relationship("Application", back_populates="owner", cascade="all, delete")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, default=ApplicationStatus.APPLIED)
    job_url = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    applied_date = Column(DateTime(timezone=True), nullable=True)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign key linking application to its owner
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="applications")

    # One application can have one AI analysis
    analysis = relationship("Analysis", back_populates="application",
                          uselist=False, cascade="all, delete")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    fit_score = Column(Float, nullable=True)          # 0.0 to 1.0
    matched_keywords = Column(Text, nullable=True)     # stored as comma-separated
    missing_keywords = Column(Text, nullable=True)     # stored as comma-separated
    extracted_skills = Column(Text, nullable=True)     # skills found in JD
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    application = relationship("Application", back_populates="analysis")