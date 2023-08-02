from pydantic import BaseModel, root_validator, Field
from typing import List, Dict 
from uuid import uuid4
import random
from random import randint
import json


from pathlib import Path
current_path = Path(__file__).parent
parent_directory = current_path.parent
json_path = parent_directory / "data_bases" / "biometrics.json"

class biometric(BaseModel):
    """
    Represents a detailed biometric profile for an individual.

    The biometric profile encompasses a wide range of physiological and physical characteristics 
    such as height, weight, facial features, and unique identifiers like DNA and fingerprint IDs. 
    This model is useful for applications in security, medical analysis, and personal identification.
    
    Attributes:
        _sex (str): Gender of the individual. Either 'M' for Male or 'F' for Female. Defaults to 'M'.
        height (int): Height of the individual in centimeters.
        weight (int): Weight of the individual in kilograms.
        waist (int): Waist measurement of the individual in centimeters.
        chest_circumference (int): Chest circumference of the individual in centimeters.
        foot_size (int): Shoe size of the individual.
        hair_length (str): Length of the individual's hair. Can be values like "Short", "Medium", etc.
        hair_color (str): Color of the individual's hair.
        eye_color (str): Color of the individual's eyes.
        face_shape (str): Shape of the individual's face. Can be values like "Oval", "Round", etc.
        ear_shape (str): Shape of the individual's ears.
        nose_shape (str): Shape of the individual's nose.
        lip_shape (str): Shape of the individual's lips.
        dental_records (str): Details or codes representing the individual's dental records.
        blood_type (str): Blood type of the individual.
        gait_pattern (str): The walking pattern of the individual.
        voice_id (str): A unique identifier for the individual's voice.
        dna_id (str): A unique identifier for the individual's DNA.
        fingerprint_id (str): A unique identifier for the individual's fingerprint.
        retina_scan_id (str): A unique identifier for the individual's retina scan.
        handwriting_sample_id (str): A unique identifier for the individual's handwriting sample.
        birthmarks (List[str]): A list of descriptions of any birthmarks the individual might have.
        tattoos (Dict[str, str]): Descriptions and locations of any tattoos on the individual.
        scars (Dict[str, str]): Descriptions and locations of any scars on the individual.
        allergies (List[str]): A list of any known allergies the individual might have.
    
    Returns:
        biometric: An instance of the biometric profile with attributes populated based on the given 
                   input or defaults from a JSON data source.    

    Example:
        >>> bio = biometric()
        >>> print(bio.height)
        175
        >>> print(bio.eye_color)
        Brown
    """
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
    
    
    class Config:
        schema_extra = {
            "example": {
                "_sex": "M",
                "height": 175,
                "weight": 68,
                "waist": 32,
                "chest_circumference": 96,
                "foot_size": 42,
                "hair_length": "Short",
                "hair_color": "Black",
                "eye_color": "Brown",
                "face_shape": "Oval",
                "ear_shape": "Round",
                "nose_shape": "Straight",
                "lip_shape": "Thin",
                "dental_records": "A1B2",
                "blood_type": "A+",
                "gait_pattern": "Normal",
                "voice_id": "example-uuid",
                "dna_id": "example-uuid",
                "fingerprint_id": "example-uuid",
                "retina_scan_id": "example-uuid",
                "handwriting_sample_id": "example-uuid",
                "birthmarks": ["Mole on cheek"],
                "tattoos": {
                    "location": "Forearm",
                    "description": "Dragon"
                },
                "scars": {
                    "location": "Leg",
                    "description": "Surgical scar"
                },
                "allergies": ["Peanuts", "Dust"]
            }
        }
    
    
    @property
    def sex(self):
        return self._sex
    
    @staticmethod
    def set_id() -> str:
        return str(uuid4())
        
    
    @root_validator(pre=True)
    def set_data(cls, values):
        biometric_data = json.load(open(json_path,"r"))
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
    
