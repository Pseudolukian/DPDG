from pydantic import BaseModel

class job_specs(BaseModel):
    specialty:str = None
    position:str = None
    responsibilities:str = None