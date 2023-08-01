from pydantic import BaseModel
from data_structures.file_models import persone, passport, address,expirience,contacts, diploma, driverlicense, biometric

class OutputModel(BaseModel):
    """
    Represents a comprehensive model that aggregates individual data components from various domains.
    
    This model serves as a primary schema for the `Buffer` class. The main objective of `OutputModel` is to 
    validate and maintain data integrity across multiple data domains, such as personal information, passport details, 
    contact data, and more. By using this model, we ensure that data added to the `Buffer` aligns with expected 
    formats and structures.

    Attributes:
        - Personal_data (persone): Personal details of an individual.
        - Passport_data (passport): Passport-related details.
        - Address_data (address): Address-related information.
        - Expirience_data (expirience): Professional experience and background.
        - Contacts_data (contacts): Communication-related details, including social media and contact numbers.
        - Diploma_data (diploma): Educational background and qualifications.
        - Driver_license_data (driverlicense): Driving license-related information.
        - Biometrics_data (biometric): Biometric details like fingerprints or facial data.

    Note:
        - This model is tightly coupled with the `Buffer` class to ensure that any data added to the buffer 
        adheres to the predefined schemas for each data domain.
        - The `Config` class is used to exclude any attributes set to None from the model's output, thus ensuring clean 
        and concise data representation.
    """
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
        schema_extra = {
            "example": {
                "Personal_data": {"name": "John Doe", "age": 30},
                "Passport_data": {"passport_no": "XYZ123456", "issue_date": "2020-01-01"},
                "Address_data": {"street": "123 Main St", "city": "Springfield"},
                "Expirience_data": {"cur_position": "Engineer", "cur_company": "TechCorp"},
                "Contacts_data": {"phone_number": "+1234567890", "email": "johndoe@example.com"},
                "Diploama_data": {"specialty": "Engineering", "university": "Tech University"},
                "Driver_license_data": {"license_number": "D1234567", "categories": ["A", "B"]},
                "Biometrics_data": {"fingerprint": "ABCDEFG", "retina_scan": "XYZABC"}
            }
        }