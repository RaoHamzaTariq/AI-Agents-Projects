from pydantic import BaseModel
from typing import List

# --- PYDANTIC DATA MODELS ---
# These models define the structure for the extracted resume data and the evaluation score.

class ExperienceModel(BaseModel):
    job_title: str = None
    company: str = None
    start_date: str = None
    end_date: str = None
    duration: int = None

class EducationModel(BaseModel):
    degree: str = None
    institution: str = None
    start_year: int = None
    end_year: int = None
    duration: int = None


class ResumeModel(BaseModel):
    name: str = None
    role: str = None
    email: str = None
    phone: str = None
    other_links: List[str] = None
    skills: List[str] = None
    experience: List[ExperienceModel] = None
    education: List[EducationModel] = None
    projects: List[str] = None
    languages: List[str] = None
    certifications: List[str] = None

class EvaluationScoreModel(BaseModel):
    score: float =None
    system_score: float =None
    feedback: str =None
