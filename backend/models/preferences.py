from pydantic import BaseModel, EmailStr

class JobPreferences(BaseModel):
    job_role: str
    location: str
    experience: str | None = 0
    work_mode: str  | None = ""
    email: EmailStr
