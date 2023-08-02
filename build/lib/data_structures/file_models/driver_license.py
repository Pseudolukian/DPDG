from pydantic import BaseModel, root_validator
from typing import List
import json
import random
from random import randint


from pathlib import Path
current_path = Path(__file__).parent
parent_directory = current_path.parent
json_path = parent_directory / "data_bases" / "driverlicense.json"

class driverlicense(BaseModel):
    """
    Represents a driver's license data model, storing information about an individual's permission to operate motor vehicles.

    Attributes:
        - license_number (str): The unique identifier of the license.
        - categories (List[str]): Categories or classes of vehicles the individual is authorized to drive.
        - issue_date (str): The date the license was issued.
        - expiration_date (str): The date the license expires.
        - issuing_authority (str): The entity that issued the license.
        - restrictions (List[str]): Any restrictions applied to the license.

    The data is populated using pre-set configurations from a JSON file.

    Example:
        >>> dr_l = driverlicense()
        >>> print(dr_l)
        driverlicense(license_number='52 427-760-830 02', categories=['D - Buses'], 
        issue_date='08.01.2002', expiration_date='07.31.2029', issuing_authority='DPS - Department of Public Safety', 
        restrictions=['02 - Hearing aid or prosthetic device required', '03 - Prosthetic limb(s) required'])
    ```

    Returns:
    - A `driverlicense` instance with randomly generated attributes based on the data from the configuration file.
    """
    license_number: str = None
    categories: List[str] = []
    issue_date: str = None
    expiration_date: str = None
    issuing_authority: str = None
    restrictions: List[str] = []
    
    class Config:
        schema_extra = {
            "example": {
                "license_number": "52 427-760-830 02",
                "categories": ["D - Buses"],
                "issue_date": "01.01.2020",
                "expiration_date": "01.01.2025",
                "issuing_authority": "Department of Motor Vehicles",
                "restrictions": ["02 - Hearing aid or prosthetic device required", 
                                 "03 - Prosthetic limb(s) required"]
            }
        }
    
    @root_validator(pre = True)
    def set_driverlicense_data(cls, values):
        driverlicense_data = json.load(open(json_path,"r"))
        lic_num = [str(x).replace("X",str(randint(0,9))) for x in driverlicense_data["license_number_template"]]
        values["license_number"] = "".join(lic_num)
        rand_categories = list(set(random.choices(driverlicense_data["categories"], k = randint(1,3))))
        values["categories"] = rand_categories
        issuing_auth_list = driverlicense_data["issuing_authority"]
        restrictions_list = list(set(random.choices(driverlicense_data["restrictions"], k = randint(0,2))))
        values["issuing_authority"] = random.choice(issuing_auth_list)
        values["restrictions"] = restrictions_list
        return values
        