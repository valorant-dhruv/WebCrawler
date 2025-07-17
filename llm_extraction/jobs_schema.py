from pydantic import BaseModel, Field
from typing import List, Optional


class JobPosting(BaseModel):
    """Basic job posting model"""
    company: str = Field(description="Company name")
    position: str = Field(description="Job position/title")
    location: Optional[str] = Field(description="Job location (remote, city, etc.)")
    technologies: List[str] = Field(description="Technologies, programming languages, frameworks mentioned")
    contact_info: Optional[str] = Field(description="Contact email or application instructions")


class JobPostings(BaseModel):
    """Container for multiple job postings"""
    jobs: List[JobPosting] = Field(description="List of job postings")