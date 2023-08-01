from pydantic import BaseModel, Field, root_validator
from random import random
import random

import json

class passport(BaseModel):
    """
    A model that represents a passport with essential details.
    
    Attributes:
        - date_of_birth (str): Date of birth of the passport holder.
        - sex (str): Gender of the passport holder. Defaults to "M". Choices are "M" or "F".
        - country (str): The issuing country of the passport. Defaults to "USA". Other choices are "RUSSIA" and "UK".
        - passport_number (str): A unique identifier for the passport.
        - issue_date (str): Date on which the passport was issued.
        - expiration_date (str): Date on which the passport expires.
        - authority (str): Issuing authority of the passport.
    
    Methods:
        - generate_passport_number: Generates a random passport number based on the template.
        - set_def_vals: A root validator that sets default values for certain fields.
    
    Example:
        >>> pas = passport()
        >>> print(pas)
        passport(date_of_birth='08.01.1957', sex='F', country='USA', 
        passport_number='57404-38195', issue_date='08.01.1973', 
        expiration_date='08.01.2013', authority='U.S. Department of State')
    """
    date_of_birth: str = None
    sex:str = Field(default="M", choices=["M","F"])
    country:str = Field(default="USA", choices=["USA", "RUSSIA", "UK"])
    passport_number:str = None
    issue_date:str = None
    expiration_date:str = None
    authority:str = None
    
    class Config:
        schema_extra = {
            "example": {
                "date_of_birth": "1990-01-01",
                "sex": "M",
                "country": "USA",
                "issue_date": "2010-01-01",
                "expiration_date": "2020-01-01",
                "authority": "US Department of State"
            }
        }
        
    @staticmethod
    def generate_passport_number(template: str) -> str:
        """
        Generates a random passport number based on the provided template.
        
        Args:
        - template (str): A string with 'X' placeholders for digits.
        
        Returns:
        - str: A generated passport number.
        """
        result = []
        for char in template:
            if char == 'X':
                result.append(str(random.randint(0, 9)))
            else:
                result.append(char)
        return ''.join(result)
    
    
    @root_validator(pre=True)
    def set_def_vals(cls, values):
        """
        A root validator that sets default values for authority and passport number 
        based on the selected country.
        
        Args:
        - values (dict): Contains all the fields of the passport model.
        
        Returns:
        - dict: Updated fields of the passport model.
        """
        
        passport_data = json.load(open("./data_structures/data_bases/passport.json"))
        pass_num = passport_data[values["country"]]["passport_temp_number"]
        auth = random.choice(passport_data[values["country"]]["authority"])
        values["authority"] = auth
        values["passport_number"] = cls.generate_passport_number(pass_num)

        return values

