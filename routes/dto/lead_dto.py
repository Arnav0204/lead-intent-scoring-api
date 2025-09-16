from pydantic import BaseModel , Field


class LeadDTO(BaseModel):
    name         : str  = Field(...,min_length=1)
    role         : str  = Field(...,min_length=1,max_length=100)
    company      : str  = Field(...,min_length=1,max_length=50)
    industry     : str  = Field(...,min_length=1,max_length=50)
    location     : str  = Field(...,min_length=1,max_length=50)
    linkedin_bio : str  = Field(...,min_length=1,max_length=500)
