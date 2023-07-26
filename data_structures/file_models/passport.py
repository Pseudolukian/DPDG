from pydantic import BaseModel, Field, validator,root_validator
from random import randint, random
import random

import json

class passport(BaseModel):
    date_of_birth: str = None
    sex:str = Field(default="M", choices=["M","F"])
    country:str = Field(default="USA", choices=["USA", "RUSSIA", "UK"])
    passport_number:str = None
    issue_date:str = None
    expiration_date:str = None
    authority:str = None
    
    
    @staticmethod
    def generate_passport_number(template: str) -> str:
        result = []
        for char in template:
            if char == 'X':
                result.append(str(random.randint(0, 9)))
            else:
                result.append(char)
        return ''.join(result)
    
    
    @root_validator(pre=True)
    def set_def_vals(cls, values):
        
        #======Set thr passport number=======#
        passport_data = json.load(open("./data_structures/data_bases/passport.json"))
        pass_num = passport_data[values["country"]]["passport_temp_number"]
        auth = random.choice(passport_data[values["country"]]["authority"])
        values["authority"] = auth
        values["passport_number"] = cls.generate_passport_number(pass_num)

        return values

