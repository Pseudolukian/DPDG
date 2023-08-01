from pydantic import BaseModel, root_validator
from typing import List
import json
import random
from random import randint

class expirience(BaseModel):
    """
    Represents an individual's work experience, encompassing details about their current and previous positions.

    Attributes:
        - _country (str): The country of the company where the person works or worked.
        - cur_position (str): Current position or job title.
        - cur_company (str): The current company's name.
        - cur_comp_start_date (str): The starting date of employment at the current company.
        - responsibilities (List[str]): List of job responsibilities in the current position.
        - work_phone (str): Work contact number.
        - supervisor_name (str): Name of the current supervisor or manager.
        - salary (int): Current salary.
        - currency (str): Currency in which the salary is paid.
        - awards (List[str]): Awards received during the tenure at the current company.
        - reprimands (List[str]): Reprimands received during the tenure at the current company.
        - prev_company (str): Previous company's name.
        - prev_position (str): Position or job title at the previous company.
        - prev_comp_start_date (str): The starting date of employment at the previous company.
        - reason_for_leaving (str): Reason for leaving the previous company.

    The data is populated using pre-set configurations from a JSON file based on the _country attribute.

    Example:
        >>> exp = expirience()
        >>> print(exp)
        expirience(cur_position='Environmental Scientist', cur_company='HSBC', 
        cur_comp_start_date='07.31.2020', responsibilities=['Study environmental problems', 'Advise on sustainability'], 
        work_phone='+44 1881-687-591', supervisor_name='Charlie Thomas', salary=1625, currency='GBP', 
        awards=['Employee of the Month', 'Best Innovator Award'], reprimands=['None reprimands'], 
        prev_company='BP', prev_position='Laboratory Technician', prev_comp_start_date='08.01.2018', 
        reason_for_leaving='Personal reasons')

    Returns:
        - An expirience instance with randomly generated attributes based on the data from the configuration file.
    """
    _country:str = None
    cur_position: str = None
    cur_company: str = None
    cur_comp_start_date: str = None
    responsibilities: List[str] = []
    work_phone: str = None
    supervisor_name: str = None
    salary: int = None
    currency:str = None
    awards: List[str] = []
    reprimands: List[str] = []
    
    prev_company: str = None
    prev_position: str = None
    prev_comp_start_date:str = None
    reason_for_leaving: str = None
    
    class Config:
        schema_extra = {
            "example": {
                "_country": "USA",
                "cur_position": "Software Developer",
                "cur_company": "Tech Corp",
                "cur_comp_start_date": "01-01-2019",
                "responsibilities": ["Develop software", "Maintain code"],
                "work_phone": "+44 1881-687-591",
                "supervisor_name": "John Doe",
                "salary": 5000,
                "currency": "USD",
                "awards": ["Best Developer 2020"],
                "reprimands": ["None reprimands"],
                "prev_company": "Old Tech Corp",
                "prev_position": "Junior Developer",
                "prev_comp_start_date": "01.01.2018",
                "reason_for_leaving": "Better Opportunity"
            }
        }
        
    @staticmethod
    def generate_phone_number(pattern: str) -> str:
        return ''.join(str(random.randint(0, 9)) if char == 'X' else char for char in pattern)

    @property
    def country(self):
        return self._country
    
    
    @root_validator(pre=True)
    def set_exp_data(cls, values):
        exp_data = json.load(open("./data_structures/data_bases/expirience.json"))
        contacts_data = json.load(open("./data_structures/data_bases/contacts.json", "r"))
        rand_cur_comp = random.choice(exp_data[values["country"]]["companies"])
        rand_prev_comp = random.choice(exp_data[values["country"]]["companies"])
        
        values["cur_company"] = rand_cur_comp
        values["prev_company"] = rand_prev_comp
        values["work_phone"] = cls.generate_phone_number(contacts_data["phone_templates"][values["country"]])
        if values["country"] == "USA":
            values["salary"] = randint(2000, 8000)
            values["currency"] = "USD"
        elif values["country"] == "RUSSIA":
            values["salary"] = randint(50000, 200000)
            values["currency"] = "RUB"
        elif values["country"] == "UK":
            values["salary"] = randint(1500, 6500)
            values["currency"] = "GBP"   
            
        if random.random() < 0.3:
            rand_awards = ["Now awards yeat."]
            values["awards"] = rand_awards
            rand_reprimands = list(set(random.choices(exp_data["reprimands"], k=3)))
            values["reprimands"] = rand_reprimands
        else:
            rand_awards = list(set(random.choices(exp_data["awards"], k=2)))
            values["awards"] = rand_awards
            values["reprimands"] = ["None reprimands"]
                
        
        values["reason_for_leaving"] = random.choice(exp_data["reason_for_leaving"])
        return values
    