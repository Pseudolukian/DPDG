from pydantic import BaseModel, root_validator
from typing import Optional
import json
from random import randint
import random

from pathlib import Path
current_path = Path(__file__).parent
parent_directory = current_path.parent
json_path = parent_directory / "data_bases" / "addresses_base.json"



class address(BaseModel):
    """
    Represents an address structure with various attributes.

    The class is designed to model an address, including country, administrative division,
    city, street, house number, apartment number, and postal code. It provides methods to generate 
    random address components based on specified patterns and set address data from predefined data.

    Attributes:
        _country (str): The country of the address. It's a private attribute.
        administrative_division (Optional[str]): The administrative division/state of the address.
        city (Optional[str]): The city of the address.
        street (Optional[str]): The street of the address.
        house_number (Optional[str]): The house number of the address.
        apartment_number (Optional[str]): The apartment number of the address.
        postal_code (Optional[str]): The postal code of the address.

    Returns:
        address: An instance representing a structured address.
    
    Example:
        >>> addr_example = address(
        ...     country="USA",
        ...     administrative_division="California",
        ...     city="Los Angeles",
        ...     street="Hollywood Blvd",
        ...     house_number="123",
        ...     apartment_number="101",
        ...     postal_code="90028"
        ... )
        >>> print(addr_example.city)
        Los Angeles
    """
    _country:str = None
    administrative_division: Optional[str] = None
    city: Optional[str]  = None
    street: Optional[str]  = None
    house_number: Optional[str]  = None
    apartment_number: Optional[str]  = None
    postal_code: Optional[str]  = None
    
    
    class Config:
        schema_extra = {
            "example": {
                "country": "USA",
                "administrative_division": "California",
                "city": "Los Angeles",
                "street": "Hollywood Blvd",
                "house_number": "123",
                "apartment_number": "101",
                "postal_code": "90028"
            }
        }

    @property
    def country(self):
        return self._country
    
    @staticmethod
    def generate_from_pattern(pattern: str) -> str:
        return ''.join(str(random.randint(0, 9)) if char == 'X' else char for char in pattern)
    
    
    @root_validator(pre=True)
    def set_data(cls, values):
        coun = values.get("country", "USA")
        addresses_data = json.load(open(json_path,"r"))
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