from fastapi import FastAPI, HTTPException, Query
from database import db_profile
import crud
from schemas import Profile
from typing import List

app = FastAPI(title="Api backend for Me-Api Playground")

"""
----------------------------------------
Basic Health Check Endpoint && App Initialization
----------------------------------------
"""
#health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

""""
----------------------------------------
CRUD Endpoints for Profile Management
----------------------------------------
"""
# Create Profile
@app.post("/profile", response_model=Profile)
def create_profile(profile: Profile):
    if db_profile is not None:
        raise HTTPException(status_code=400, detail="Profile already exists. Use update endpoint to modify.")
    created_profile = crud.create_profile(profile)
    return created_profile

# Get Profile
@app.get("/profile", response_model=Profile)
def get_profile():
    profile = crud.get_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile

# Update Profile
@app.put("/profile", response_model=Profile)
def update_profile(updated_profile: Profile):
    profile = crud.update_profile(updated_profile)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found. Create a profile first.")
    return profile

'''
----------------------------------------
Query Endpoints for Specific Data Retrieval
----------------------------------------
'''
# Get Projects
@app.get("/projects", response_model=List[Profile])
def get_projects(skill: str | None = None):
    if not db_profile:
        raise HTTPException(404, "Profile not found")

    projects = db_profile.projects
    if skill:
        projects = [
            p for p in projects
            if skill.lower() in db_profile.skills
        ]
    return projects

#Skills Endpoint
@app.get("/skills/top")
def top_skills(limit: int = 5):
    if not db_profile:
        raise HTTPException(404, "Profile not found")

    skills = db_profile.skills
    return skills[:limit]

#search
@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    if not db_profile:
        raise HTTPException(404, "Profile not found")

    q = q.lower()

    results = {
        "skills": [s for s in db_profile.skills if q in s.lower()],
        "projects": [
            p for p in db_profile.projects
            if q in p.title.lower() or q in p.description.lower()
        ],
        "work": [
            w for w in db_profile.work
            if q in w.company.lower() or q in w.role.lower()
        ]
    }
    return results

