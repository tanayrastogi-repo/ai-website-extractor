from pydantic import BaseModel, Field
from typing import Optional

class JobInfo(BaseModel):
    """Structured information about a job posting."""
    job_title: str = Field(description="The official title of the job position.")
    company_name: str = Field(description="The name of the company offering the job.")
    location: str = Field(description="The geographic location of the job (e.g., 'Remote', 'New York, NY').")
    about_company: str = Field(description="A brief description of what the company does.")
    key_responsibilities: str = Field(description="Main duties and tasks the employee will perform.")
    qualifications: list[str] = Field(description="Educational background, certifications, or years of experience required, as a list of bullet points.")
    technical_skills: list[str] = Field(description="List of specific technical skills, tools, or knowledge needed for the role.")
    soft_skills: list[str] = Field(description="List of soft skills, such as communication, leadership, or teamwork, needed for the role.")
    contact_person: Optional[str] = Field(description="Name or role of the person to contact, if available.")
