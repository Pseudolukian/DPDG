from pydantic import BaseModel
from models import persone, passport, address,expirience,contacts, diploma, driverlicense, biometric

class OutputModel(BaseModel):
    Personal_data:persone = None
    Passport_data:passport = None
    Address_data:address = None
    Expirience_data:expirience = None
    Contacts_data:contacts = None
    Diploama_data:diploma = None
    Driver_license_data:driverlicense = None
    Biometrics_data:biometric = None
    
    class Config:
        exclude_none = True
        