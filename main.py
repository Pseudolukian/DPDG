from models import *
from config import *
from pprint import pprint

import random
from random import randint
from typing import List



def fakir(country:str = "USA", sex:str = "M", age:List[int] = [25,70], date_template:str = importer()):
    random_age = randint(age[0],age[1])
    random_spec_pos_resp = rand_spec_pos_resp()
    cur_job_start = random_date(way="past", delta=[1,3])
    prev_job_start = random_date(way="past", delta=[3,5])
    #=======Personal data===============
    pers = persone(country = country, 
                   sex = sex,
                   age = random_age)
    #=======Passport data===============
    pas = passport(country = country, sex = sex, 
                   date_of_birth = day_of_birth(age=random_age, date_template=date_template),
                   issue_date = day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=16),
                   expiration_date = day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=56))
    
    #=======Address data===============
    ad = address(country = country)
    
    #=======Expirience data=============
    supervisor = persone(country = country, sex = sex)
    exp = expirience(country = country, 
                     cur_position = random_spec_pos_resp.position,
                     responsibilities = random_spec_pos_resp.responsibilities,
                     cur_comp_start_date = cur_job_start,
                     supervisor_name = "".join(supervisor.name + " " + supervisor.last_name),
                     prev_position = rand_spec_pos_resp().position,
                     prev_comp_start_date = prev_job_start)
    
    #=======Contacts data===============
    cont = contacts(country = country, sex = sex)
    #=======Diploama data===============
    thes_ad = persone(country = country, sex = sex)
    diplom = diploma(thesis_advisor = "".join(thes_ad.name + " " + thes_ad.last_name),
                     specialty = random_spec_pos_resp.specialty,
                     graduation_year=day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=22))
    
    #=======Driver license data===============
    dr_lic = driverlicense(issue_date = day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=18), 
                           expiration_date = random_date(way="future", delta=[5,10]))
    
    #=======Biometrics data===============
    bio = biometric(sex = sex)
    
    out_full = {"Personal data":pers.dict(),
                "Passport data":pas.dict(),
                "Address data":ad.dict(),
                "Expirience data":exp.dict(),
                "Contacts data":cont.dict(),
                "Diploama data":diplom.dict(),
                "Driver license data":dr_lic.dict(),
                "Biometrics data": bio.dict()
                }
    return out_full


pprint(fakir())
