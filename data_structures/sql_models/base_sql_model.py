from sqlmodel import Field, SQLModel, Relationship 
from typing import Optional 
from uuid import UUID

class persone(SQLModel, table = True):
    personal_id:UUID = Field(primary_key=True)
    name:str = None
    last_name:str = None
    age:int = None

    passport_id: Optional["passport"] = Relationship(back_populates="persone_ref")
    address_id: Optional["address"] = Relationship(back_populates="persone_ref")
    driverlicense_id: Optional["driverlicense"] = Relationship(back_populates="persone_ref")
    contacts_id: Optional["contacts"] = Relationship(back_populates="persone_ref")
    diploma_id: Optional["diploma"] = Relationship(back_populates="persone_ref")
    expirience_id: Optional["expirience"] = Relationship(back_populates="persone_ref")
    biometric_id: Optional["biometric"] = Relationship(back_populates="persone_ref")
    


class passport(SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True) 
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    date_of_birth: str = None
    sex:str = None
    country:str = None
    passport_number:str = None
    issue_date:str = None
    expiration_date:str = None
    authority:str = None
    
    persone_ref: "persone" = Relationship(back_populates="passport_id")


class driverlicense( SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    license_number: str = None
    categories: str = None
    issue_date: str = None
    expiration_date: str = None
    issuing_authority: str = None
    restrictions: str = None   
    
    persone_ref: "persone" = Relationship(back_populates="driverlicense_id")
    
class address( SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    administrative_division: Optional[str] = None
    city: Optional[str]  = None
    street: Optional[str]  = None
    house_number: Optional[str]  = None
    apartment_number: Optional[str]  = None
    postal_code: Optional[str]  = None    
    
    persone_ref: "persone" = Relationship(back_populates="address_id")
    
class contacts( SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    phone_number:str = None
    nick_name:str = None
    email:str = None
    facebook_link:str = None
    vkontakte_link:str = None
    LinkedIn_link:str = None
    Telegram_link:str = None    
    
    persone_ref: "persone" = Relationship(back_populates="contacts_id")
    
class diploma( SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    specialty: str = None
    qualification: str  = None
    graduation_year: str = None
    university: str = None
    diploma_number: Optional[str] = None
    gpa: Optional[float]  = None
    honors: Optional[str]  = None
    thesis_title: Optional[str]  = None
    thesis_advisor: Optional[str] = None 
    
    persone_ref: "persone" = Relationship(back_populates="diploma_id") 
    
class expirience(SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    cur_position: str = None
    cur_company: str = None
    cur_comp_start_date: str = None
    responsibilities: str = None
    work_phone: str = None
    supervisor_name: str = None
    salary: int = None
    currency:str = None
    awards: str = None
    reprimands: str = None
    
    prev_company: str = None
    prev_position: str = None
    prev_comp_start_date:str = None
    reason_for_leaving: str = None    
    
    persone_ref: "persone" = Relationship(back_populates="expirience_id")


class biometric( SQLModel, table = True):
    id:Optional[int] = Field(default= None, primary_key= True)
    to_personal_id: Optional[UUID] = Field(default= None, foreign_key="persone.personal_id")
    height: int = None
    weight: int = None
    waist: int = None
    chest_circumference: int = None
    foot_size: int = None
    hair_length: str = None
    hair_color: str = None
    eye_color: str = None
    face_shape: str = None
    
    ear_shape: str = None
    nose_shape: str = None
    lip_shape: str = None
    dental_records: str = None
    blood_type: str = None
    gait_pattern: str = None
    voice_id: str = None
    dna_id: str = None
    fingerprint_id: str = None
    retina_scan_id: str = None
    handwriting_sample_id: str = None
    birthmarks: str = None
    tattoos: str = None
    scars: str = None
    allergies: str = None    
    
    persone_ref: "persone" = Relationship(back_populates="biometric_id")
    
