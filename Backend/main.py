from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
import models
import schemas

app = FastAPI(title="API backend for Me-API Playground")


@app.middleware("http")
async def _ensure_cors_headers(request, call_next):
    """Ensure CORS headers are present even on errors."""
    response = await call_next(request)
    response.headers.setdefault("Access-Control-Allow-Origin", "*")
    response.headers.setdefault("Access-Control-Allow-Headers", "*")
    response.headers.setdefault("Access-Control-Allow-Methods", "*")
    return response


def _get_profile_or_404(db: Session, name: Optional[str]):
    """Return profile filtered by name (case-insensitive, trimmed, partial) or the first profile."""
    if name:
        trimmed = name.strip()
        if not trimmed:
            profile = db.query(models.Profile).first()
        else:
            lowered = trimmed.lower()
            profile = (
                db.query(models.Profile)
                .filter(func.lower(models.Profile.name) == lowered)
                .first()
            )
            if not profile:
                profile = (
                    db.query(models.Profile)
                    .filter(models.Profile.name.ilike(f"%{trimmed}%"))
                    .first()
                )
    else:
        profile = db.query(models.Profile).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

"""
----------------------------------------
Health Check
----------------------------------------
"""
@app.get("/health")
def health_check():
    return {"status": "ok"}

'''
----------------------------------------
use this for local testing
----------------------------------------
'''

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app)
'''
----------------------------------------
for serverless deployment
----------------------------------------
'''
from mangum import Mangum
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
----------------------------------------
Profile CRUD
----------------------------------------
"""

# Create Profile
@app.post("/profile", response_model=schemas.ProfileOut)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = models.Profile(
        name=profile.name,
        email=profile.email,
        education=profile.education,
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


# Get Profile
@app.get("/profile", response_model=schemas.ProfileOut)
def get_profile(name: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return _get_profile_or_404(db, name)


# Update Profile
@app.put("/profile", response_model=schemas.ProfileOut)
def update_profile(
    profile: schemas.ProfileUpdate,
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    db_profile = _get_profile_or_404(db, name)

    db_profile.name = profile.name
    db_profile.email = profile.email
    db_profile.education = profile.education

    db.commit()
    db.refresh(db_profile)
    return db_profile


"""
----------------------------------------
Query Endpoints
----------------------------------------
"""

# Get Projects (optionally filtered by skill)
@app.get("/projects")
def get_projects(
    skill: Optional[str] = None,
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    profile = _get_profile_or_404(db, name)

    projects = profile.projects

    if skill:
        if skill.lower() not in [s.name.lower() for s in profile.skills]:
            return []

    return projects


# Top Skills
@app.get("/skills/top")
def top_skills(
    limit: int = 5,
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    profile = _get_profile_or_404(db, name)

    return [s.name for s in profile.skills][:limit]


# Search
@app.get("/search")
def search(
    q: str = Query(..., min_length=1),
    name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    profile = _get_profile_or_404(db, name)

    q = q.lower()

    return {
        "skills": [
            s.name for s in profile.skills
            if q in s.name.lower()
        ],
        "projects": [
            p for p in profile.projects
            if q in p.title.lower() or q in p.description.lower()
        ],
        "work": [
            w for w in profile.work
            if q in w.company.lower() or q in w.role.lower()
        ]
    }
