from datetime import date
from pydantic import BaseModel, root_validator
from typing import Optional
import json
import random
from random import randint
from datetime import datetime



class diploma(BaseModel):
    specialty: str = None
    qualification: str  = None # Например, "Bachelor of Science", "Магистр" и т.д.
    graduation_year: str = None
    university: str = None
    diploma_number: Optional[str] = None
    gpa: Optional[float]  = None # Средний балл (Grade Point Average)
    honors: Optional[str]  = None # Например, "cum laude", "с отличием" и т.д.
    thesis_title: Optional[str]  = None # Название дипломной работы или проекта
    thesis_advisor: Optional[str] = None # Научный руководитель (если есть)
    
    
    @staticmethod
    def generate_diploma_number(template: str) -> str:
        result = []
        for char in template:
            if char == 'x':
                result.append(str(random.randint(0, 9)))
            else:
                result.append(char)
        return ''.join(result)

    @root_validator(pre = True)
    def set_diploma_data(cls,values):
        diploma_data = json.load(open("./data_structures/diploma.json","r"))
        values["qualification"] = random.choice(diploma_data["qualification"])
        values["university"] = random.choice(diploma_data["university"])
        values["honors"] = random.choice(diploma_data["honors"])
        values["thesis_title"] = random.choice(diploma_data["thesis_title"])
        diploma_number_template = "xx-xxx-xx"
        diploma_number_generate = cls.generate_diploma_number(diploma_number_template)
        values["diploma_number"] = diploma_number_generate
        values["gpa"] = randint(2.0,5.0)
        return values