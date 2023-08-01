from pydantic import BaseModel, root_validator, Field
import json
import random
from uuid import uuid4

class persone(BaseModel):
    """
    A model representing personal details of an individual.
    
    Attributes:
        - personal_id (str): A unique identifier for the individual, generated using uuid.
        - _sex (str): Gender of the individual. Internal representation. Defaults to "M". Choices are "M" or "F".
        - _country (str): Country of the individual. Internal representation. Defaults to "USA". Other choices are "RUSSIA" and "UK".
        - name (str): First name of the individual.
        - last_name (str): Last name/surname of the individual.
        - age (int): Age of the individual.
    
    Properties:
        - sex: Returns the gender of the individual.
        - country: Returns the country of the individual.
    
    Methods:
        - set_persone_data: A root validator that sets the name and last name based on gender and country.
    Example:
        >>> pers = persone()
        >>> print(pers)
        persone(personal_id=UUID('65685aba-97cd-4a72-9535-6a302bf56715'), name='Lucy', last_name='White', age=66)
    """
    
    personal_id:str = Field(default_factory=uuid4)
    _sex:str = Field(default="M", choices = ["M","F"])
    _country:str = Field(default="USA",choices = ["USA","RUSSIA","UK"])
    name:str = None
    last_name:str = None
    age:int = None
    
    class Config:
        schema_extra = {
            "example": {
                "personal_id": "65685aba-97cd-4a72-9535-6a302bf56715",
                "_sex": "M",
                "_country": "USA",
                "age": 30
            }
        }
    
    @property
    def sex(self):
        return self._sex
    
    @property
    def country(self):
        return self._country
    
    @root_validator(pre = True)
    def set_persone_data(cls, values):
        """
        A root validator that sets name and last name for the individual based on the given gender and country.
        
        Args:
            - values (dict): Contains all the fields of the persone model.
        
        Returns:
            - dict: Updated fields of the persone model.
        """
        persone_data = json.load(open("./data_structures/data_bases/persone.json","r"))
        name_data = persone_data[values["sex"]][values["country"]]["names"]
        last_name_data = persone_data[values["sex"]][values["country"]]["last_names"]
        values["name"] = random.choice(name_data)
        values["last_name"] = random.choice(last_name_data)
        return values