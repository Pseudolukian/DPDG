from pydantic import BaseModel, root_validator, Field
from typing import List, Dict, Optional
from uuid import UUID, uuid4
import random
from random import randint
import json

class biometric(BaseModel):
    _sex:str = Field(default="M", choices=["M","F"])
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
    birthmarks: List[str] = []
    tattoos: Dict[str, str] = {}
    scars: Dict[str, str] = {}
    allergies: List[str] = []
    
    
    @property
    def sex(self):
        return self._sex
    
    @staticmethod
    def set_id() -> str:
        return str(uuid4())
        
    
    @root_validator(pre=True)
    def set_data(cls, values):
        biometric_data = json.load(open("./data_structures/data_bases/biometrics.json","r"))
        #======set height===========#
        min_height = biometric_data[values["sex"]]["height"]["min_height"]
        max_height = biometric_data[values["sex"]]["height"]["max_height"]
        values["height"] = randint(min_height, max_height)
        
        #======set weight===========#
        min_weight = biometric_data[values["sex"]]["weight"]["min_weight"]
        max_weight = biometric_data[values["sex"]]["weight"]["max_weight"]
        values["weight"] = randint(min_weight, max_weight)
        
        #======set waist===========#
        min_waist = biometric_data[values["sex"]]["waist"]["min_waist"]
        max_waist = biometric_data[values["sex"]]["waist"]["max_waist"]
        values["waist"] = randint(min_waist, max_waist)
        
        #======set chest_circumference===========#
        min_chest = biometric_data[values["sex"]]["chest_circumference"]["min_chest_circumference"]
        max_chest = biometric_data[values["sex"]]["chest_circumference"]["max_chest_circumference"]
        values["chest_circumference"] = randint(min_chest, max_chest)
        
        #======set foot_size===========#
        min_foot_size = biometric_data[values["sex"]]["foot_size"]["min_foot_size"]
        max_foot_size = biometric_data[values["sex"]]["foot_size"]["max_foot_size"]
        values["foot_size"] = randint(min_foot_size, max_foot_size)
        
        # Other random choices from lists 
        values["hair_length"] = random.choice(biometric_data["hair_length"])
        values["hair_color"] = random.choice(biometric_data["hair_color"])
        values["eye_color"] = random.choice(biometric_data["eye_color"])
        values["face_shape"] = random.choice(biometric_data["face_shape"])
        values["ear_shape"] = random.choice(biometric_data["ear_shape"])
        values["nose_shape"] = random.choice(biometric_data["nose_shape"])
        values["lip_shape"] = random.choice(biometric_data["lip_shape"])
        values["dental_records"] = random.choice(biometric_data["dental_records"])
        values["blood_type"] = random.choice(biometric_data["blood_type"])
        values["gait_pattern"] = random.choice(biometric_data["gait_pattern"])
        
        # For lists with multiple options
        values["birthmarks"] = random.choices(biometric_data["birthmarks"], k=randint(0,3))
        values["allergies"] = random.choices(biometric_data["allergies"], k=randint(0,3))
        
        # For the tattoos and scars dictionaries
        values["tattoos"] = {
            "location": random.choice(biometric_data["tattoos"]["location"]),
            "description": random.choice(biometric_data["tattoos"]["description"])
        }
        values["scars"] = {
            "location": random.choice(biometric_data["scars"]["location"]),
            "description": random.choice(biometric_data["scars"]["description"])
        }
        
        #=====Set IDs=======
        for id in ["dna_id","fingerprint_id","retina_scan_id","handwriting_sample_id","voice_id"]:
            values[id] = cls.set_id()
        
        return values   
    
