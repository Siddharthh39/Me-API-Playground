from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
import models
import schemas

app = FastAPI(title="API backend for Me-API Playground")

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
    existing = db.query(models.Profile).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists. Use update endpoint."
        )

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
def get_profile(db: Session = Depends(get_db)):
    print("hello")
    profile = db.query(models.Profile).first()
    print(profile)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# Update Profile
@app.put("/profile", response_model=schemas.ProfileOut)
def update_profile(profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

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
def get_projects(skill: str | None = None, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    projects = profile.projects

    if skill:
        if skill.lower() not in [s.name.lower() for s in profile.skills]:
            return []

    return projects


# Top Skills
@app.get("/skills/top")
def top_skills(limit: int = 5, db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return [s.name for s in profile.skills][:limit]


# Search
@app.get("/search")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

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
