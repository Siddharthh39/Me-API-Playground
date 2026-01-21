from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

profile_skills = Table(
    "profile_skills",
    Base.metadata,
    Column("profile_id", ForeignKey("profiles.id")),
    Column("skill_id", ForeignKey("skills.id"))
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    education = Column(Text)

    skills = relationship("Skill", secondary=profile_skills)
    projects = relationship("Project")
    work = relationship("WorkExperience")
    links = relationship("Links", uselist=False)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    description = Column(Text)
    links = Column(Text)

class WorkExperience(Base):
    __tablename__ = "work_experience"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    company = Column(String)
    role = Column(String)
    duration = Column(String)
    description = Column(Text)

class Links(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    github = Column(Text)
    linkedin = Column(Text)
    portfolio = Column(Text)
