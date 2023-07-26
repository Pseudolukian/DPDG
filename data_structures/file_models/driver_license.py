from pydantic import BaseModel, root_validator
from typing import List
import json
import random
from random import randint
from datetime import datetime


class driverlicense(BaseModel):
    license_number: str = None
    categories: List[str] = []
    issue_date: str = None
    expiration_date: str = None
    issuing_authority: str = None
    restrictions: List[str] = []
    
    @root_validator(pre = True)
    def set_driverlicense_data(cls, values):
        driverlicense_data = json.load(open("./data_structures/data_bases/driverlicense.json","r"))
        lic_num = [str(x).replace("X",str(randint(0,9))) for x in driverlicense_data["license_number_template"]]
        values["license_number"] = "".join(lic_num)
        rand_categories = list(set(random.choices(driverlicense_data["categories"], k = randint(1,3))))
        values["categories"] = rand_categories
        issuing_auth_list = driverlicense_data["issuing_authority"]
        restrictions_list = list(set(random.choices(driverlicense_data["restrictions"], k = randint(0,2))))
        values["issuing_authority"] = random.choice(issuing_auth_list)
        values["restrictions"] = restrictions_list
        return values
        