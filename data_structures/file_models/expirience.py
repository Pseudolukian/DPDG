from pydantic import BaseModel, root_validator
from typing import List
import json
import random
from random import randint

class expirience(BaseModel):
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
    reprimands: List[str] = []  # Выговоры
    
    prev_company: str = None
    prev_position: str = None
    prev_comp_start_date:str = None
    reason_for_leaving: str = None
    
    
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
    