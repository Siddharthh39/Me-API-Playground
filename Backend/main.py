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

