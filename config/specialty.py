import json
import random
from typing import List
from pydantic import BaseModel



class job_specs(BaseModel):
    specialty:str = None
    position:str = None
    responsibilities:str = None


def rand_spec_pos_resp() -> job_specs:
    specs_out = job_specs()
    with open("./data_structures/diploma.json", "r") as file:
        spec_data = json.load(file)

    rand_spec = random.choice(list(spec_data["specialty"].keys()))
    job_positions = spec_data["specialty"][rand_spec]["job_positions"]
    job_position_dict = random.choice(job_positions)
    rand_job_pos = next(iter(job_position_dict))
    rand_resp = random.choices(job_position_dict[rand_job_pos]["responsibilities"], k=2)
    
    specs_out.specialty = rand_spec
    specs_out.position = rand_job_pos
    specs_out.responsibilities = rand_resp
    
    return specs_out
    