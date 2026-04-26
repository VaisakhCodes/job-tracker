from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from auth import get_current_user
import models
from nlp.scorer import calculate_fit_score

router = APIRouter(prefix="/analyse", tags=["AI Analyser"])


class AnalyseRequest(BaseModel):
    job_description: str
    resume_text: str
    application_id: int = None  # optional — link result to an application


class AnalyseResponse(BaseModel):
    fit_score: float
    matched_keywords: list
    missing_keywords: list
    extracted_skills: list
    match_count: int
    total_jd_keywords: int
    verdict: str


@router.post("/", response_model=AnalyseResponse)
def analyse_fit(
    request: AnalyseRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if len(request.job_description.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Job description too short — paste the full JD for accurate results"
        )

    result = calculate_fit_score(request.job_description, request.resume_text)

    # Generate a human-readable verdict
    score = result["fit_score"]
    if score >= 70:
        verdict = "Strong match — apply with confidence"
    elif score >= 50:
        verdict = "Moderate match — tailor your resume before applying"
    elif score >= 30:
        verdict = "Weak match — significant gaps to address"
    else:
        verdict = "Poor match — consider if this role fits your profile"

    # If application_id provided — save analysis to database
    if request.application_id:
        app = db.query(models.Application).filter(
            models.Application.id == request.application_id,
            models.Application.user_id == current_user.id
        ).first()

        if app:
            # Delete existing analysis if present
            if app.analysis:
                db.delete(app.analysis)
                db.commit()

            analysis = models.Analysis(
                application_id=app.id,
                fit_score=score / 100,
                matched_keywords=",".join(result["matched_keywords"]),
                missing_keywords=",".join(result["missing_keywords"]),
                extracted_skills=",".join(result["extracted_skills"])
            )
            db.add(analysis)
            db.commit()

    return {**result, "verdict": verdict}