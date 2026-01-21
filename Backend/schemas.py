from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict


class SkillOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    links: Optional[str] = None


class WorkExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None


class LinksOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None


class ProfileBase(BaseModel):
    name: str
    email: EmailStr
    education: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileOut(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    skills: List[SkillOut] = []
    projects: List[ProjectOut] = []
    work: List[WorkExperienceOut] = []
    links: Optional[LinksOut] = None

