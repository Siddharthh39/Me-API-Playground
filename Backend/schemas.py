from typing import Optional, List

from pydantic import BaseModel, EmailStr


class SkillOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    links: Optional[str] = None

    class Config:
        orm_mode = True


class WorkExperienceOut(BaseModel):
    id: int
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class LinksOut(BaseModel):
    id: int
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    education: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    id: int
    skills: List[SkillOut] = []
    projects: List[ProjectOut] = []
    work: List[WorkExperienceOut] = []
    links: Optional[LinksOut] = None

    class Config:
        orm_mode = True

