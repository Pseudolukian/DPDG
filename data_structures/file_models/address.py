from pydantic import BaseModel,Field,validator,root_validator
from typing import Optional
import json
from random import randint
import random


class address(BaseModel):
    _country:str = None
    administrative_division: Optional[str] = None
    city: Optional[str]  = None
    street: Optional[str]  = None
    house_number: Optional[str]  = None
    apartment_number: Optional[str]  = None
    postal_code: Optional[str]  = None

    @property
    def country(self):
        return self._country
    
    @staticmethod
    def generate_from_pattern(pattern: str) -> str:
        return ''.join(str(random.randint(0, 9)) if char == 'X' else char for char in pattern)
    
    
    @root_validator(pre=True)
    def set_data(cls, values):
        coun = values.get("country", "USA")
        addresses_data = json.load(open("./data_structures/data_bases/addresses_base.json","r"))
        divisions_len = len(addresses_data[coun]["states_and_cities"])-1
        random_division = randint(0, divisions_len)
        division_data = addresses_data[coun]["states_and_cities"][random_division]
        values["administrative_division"] = list(division_data.keys())[0]
        values["city"] = random.choice(list(division_data.values())[0])
        values["street"] = random.choice(addresses_data[coun]["streets"])
        house_number_pattern = random.choice(addresses_data[coun]["house_number_patterns"])
        values["house_number"] = cls.generate_from_pattern(house_number_pattern)
        postal_code_pattern = random.choice(addresses_data[coun]["postal_code_patterns"])
        values["postal_code"] = cls.generate_from_pattern(postal_code_pattern)
        values["apartment_number"] = str(randint(1, 200))
        return values