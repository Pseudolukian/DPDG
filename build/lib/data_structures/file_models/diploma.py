from pydantic import BaseModel, root_validator
from typing import Optional
import json
import random
from random import randint

from pathlib import Path
current_path = Path(__file__).parent
parent_directory = current_path.parent
json_path = parent_directory / "data_bases" / "diploma.json"


class diploma(BaseModel):
    """
    A model to represent and generate diploma details for an individual.

    The `diploma` class provides a structured representation of various diploma details for a graduate.
    It generates the qualification, university name, honors, thesis title, and diploma number based on
    predefined templates. Additionally, it has fields to represent GPA, thesis advisor, and the graduation year.

    Attributes:
        - specialty (str): The field of study or major.
        - qualification (str): The level of degree achieved (e.g., Bachelor's, Master's).
        - graduation_year (str): The year of graduation.
        - university (str): The university from which the individual graduated.
        - diploma_number (str, optional): A unique number representing the diploma.
        - gpa (float, optional): The Grade Point Average achieved during the course of study.
        - honors (str, optional): Any honors achieved during the course (e.g., cum laude).
        - thesis_title (str, optional): The title of the graduate's thesis.
        - thesis_advisor (str, optional): The name of the advisor for the graduate's thesis.

    Methods:
        generate_diploma_number(template: str) -> str:
            Generates a unique diploma number based on the provided template.

    Example:
        >>> diploma_instance = diploma()
        >>> print(diploma_instance.qualification)
        Bachelor's
    """
    specialty: str = None
    qualification: str  = None
    graduation_year: str = None
    university: str = None
    diploma_number: Optional[str] = None
    gpa: Optional[float]  = None
    honors: Optional[str]  = None
    thesis_title: Optional[str]  = None
    thesis_advisor: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "specialty": "Computer Science",
                "qualification": "Bachelor's Degree",
                "graduation_year": "2022",
                "university": "Stanford University",
                "diploma_number": "12-345-67",
                "gpa": 4.5,
                "honors": "Cum Laude",
                "thesis_title": "Efficient Algorithms in Quantum Computing",
                "thesis_advisor": "Dr. John Doe"
            }
        }
        
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
        diploma_data = json.load(open(json_path,"r"))
        values["qualification"] = random.choice(diploma_data["qualification"])
        values["university"] = random.choice(diploma_data["university"])
        values["honors"] = random.choice(diploma_data["honors"])
        values["thesis_title"] = random.choice(diploma_data["thesis_title"])
        diploma_number_template = "xx-xxx-xx"
        diploma_number_generate = cls.generate_diploma_number(diploma_number_template)
        values["diploma_number"] = diploma_number_generate
        values["gpa"] = randint(2.0,5.0)
        return values