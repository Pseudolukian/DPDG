from pydantic import BaseModel, root_validator, Field
import json
import random
from uuid import uuid4

class persone(BaseModel):
    personal_id:str = Field(default_factory=uuid4)
    _sex:str = Field(default="M", choices = ["M","F"])
    _country:str = Field(default="USA",choices = ["USA","RUSSIA","UK"])
    name:str = None
    last_name:str = None
    age:int = None
    
    @property
    def sex(self):
        return self._sex
    
    @property
    def country(self):
        return self._country
    
    @root_validator(pre = True)
    def set_persone_data(cls, values):
        persone_data = json.load(open("./data_structures/data_bases/persone.json","r"))
        name_data = persone_data[values["sex"]][values["country"]]["names"]
        last_name_data = persone_data[values["sex"]][values["country"]]["last_names"]
        values["name"] = random.choice(name_data)
        values["last_name"] = random.choice(last_name_data)
        return values
          
            
    