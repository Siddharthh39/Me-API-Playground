from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Project(BaseModel):
    id: int
    name: str
    links: Optional[List[str]] = []

class Workexp(BaseModel):
    id: int
    name: str
    role : str
    description: Optional[str] = None

class Links (BaseModel):
    github: Optional[str] = None
    linkedin: Optional[str] = None
    Leetcode: Optional[str] = None
    codeforces: Optional[str] = None

class Profile(BaseModel):
    name : str
    email : EmailStr
    education : str
    skills : List[str] = []
    Projects : List[Project] = []
    work : List[Workexp] = []
    links : Optional[Links] = None
    
