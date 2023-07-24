from models import *
import random
from random import randint
from typing import List
import json
from datetime import timedelta

from datetime import datetime
from dateutil.relativedelta import relativedelta



class FakeGenerator:
    
    def __init__(self,sex:str = "M", age:List[int] = [25,70], country:str = "USA"):
        self.sex = sex
        self.age = age
        self.country = country
        
    def config_importer(self, config_path:str = "./config/conf.json", conf_key:str = "date_format") -> str:
        """
        Loads configuration data from a JSON file and returns the value of the specified key.

        This function offers a convenient way to extract specific configuration data from a JSON file. 
        By default, it looks for the "date_format" key in the file located at "./config/conf.json".

        Args:
            config_path (str, optional): Path to the configuration JSON file. Defaults to "./config/conf.json".
            conf_key (str, optional): The key whose value is to be extracted from the JSON configuration. Defaults to "date_format".

        Returns:
            str: The value associated with the provided key from the configuration.
        """
        config_data = json.load(open(config_path,'r'))
        return config_data[conf_key]    
    
    def day_of_birth(self, age: int, date_template: str, plus_years_to_birth:int = 0) -> str:
        """
        Calculates the date of birth based on the given age and then optionally adjusts it by a number of years.

        This function first determines the date of birth from the current date minus the provided age. 
        It then optionally adds a certain number of years to the calculated date of birth, allowing for adjustments 
        or hypothetical scenarios. The resulting date is then formatted using the provided date template.

        Args:
            age (int): Age of the person for which the date of birth is to be calculated.
            date_template (str): The date format template to format the resulting date.
            plus_years_to_birth (int, optional): Number of years to add to the calculated date of birth. Defaults to 0.

        Returns:
            str: Formatted date string representing the adjusted date of birth.
        """
        date_now = datetime.now()
        date_of_birth = date_now - relativedelta(years=age)
        date_with_added_years = date_of_birth + relativedelta(years=plus_years_to_birth)
        return date_with_added_years.strftime(date_template)
    
    def random_date(self, way: str = "past", delta: List[int] = [1, 20], template:str = '%d.%M.%Y') -> str:
        """
        Generate a random date either in the past or future, based on a range of years, and then format it.

        This function takes the current date and then adjusts it by a random number of years 
        either backwards (for past dates) or forwards (for future dates). The number of adjustment 
        years is chosen randomly within a provided range. The final adjusted date is then 
        formatted according to the provided template.

        Args:
            way (str, optional): Direction of date adjustment, either "past" for dates in the past 
                or "future" for dates in the future. Defaults to "past".
            delta (List[int], optional): Range [start, end] of years to randomly select the adjustment from. 
                Defaults to [1, 20].
            template (str, optional): The date format template to format the resulting date. Defaults to '%d.%M.%Y'.

        Returns:
            str: Formatted date string representing the randomly adjusted date.

        Raises:
            ValueError: If the 'way' argument is not "past" or "future".
        """
        current_date = datetime.now()
        years_delta = random.randint(delta[0], delta[1])
        
        if way == "past":
            random_date_result = current_date - timedelta(days=365.25 * years_delta)
        elif way == "future":
            random_date_result = current_date + timedelta(days=365.25 * years_delta)
        else:
            raise ValueError(f"Invalid value for 'way': {way}. Use 'past' or 'future'.")
        
        return random_date_result.strftime(template)
    
        
    def rand_spec_pos_resp(self) -> job_specs:
        """
        Generate random job specifications including specialty, position, and responsibilities.

        This function reads from a JSON structure which has specialties and their corresponding 
        job positions along with the responsibilities for each position. It then randomly selects 
        a specialty, a job position under that specialty, and two responsibilities associated 
        with that position. These randomly selected values are stored in a `job_specs` object and returned.

        Returns:
            job_specs: An object containing the randomly selected specialty, position, 
                    and a list of two responsibilities.

        Raises:
            IOError: If there's an error reading the JSON file.
            KeyError: If the expected keys are not found in the JSON data.
        """
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
    
    
    def generator(self, chanks:List[str] = None) -> OutputModel:
        
        
        date_template = self.config_importer()
        random_age = randint(self.age[0],self.age[1])
        random_spec_pos_resp = self.rand_spec_pos_resp()
        cur_job_start = self.random_date(way="past", delta=[1,3])
        prev_job_start = self.random_date(way="past", delta=[3,5])
        
        #=======Personal data===============
        pers = persone(country = self.country, 
                    sex = self.sex,
                    age = random_age)
        #=======Passport data===============
        pas = passport(country = self.country, sex = self.sex, 
                    date_of_birth = self.day_of_birth(age=random_age, date_template=date_template),
                    issue_date = self.day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=16),
                    expiration_date = self.day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=56))
        
        #=======Address data===============
        ad = address(country = self.country)
        
        #=======Expirience data=============
        supervisor = persone(country = self.country, sex = self.sex)
        exp = expirience(country = self.country, 
                        cur_position = random_spec_pos_resp.position,
                        responsibilities = random_spec_pos_resp.responsibilities,
                        cur_comp_start_date = cur_job_start,
                        supervisor_name = "".join(supervisor.name + " " + supervisor.last_name),
                        prev_position = self.rand_spec_pos_resp().position,
                        prev_comp_start_date = prev_job_start)
        
        #=======Contacts data===============
        cont = contacts(country = self.country, sex = self.sex)
        #=======Diploama data===============
        thes_ad = persone(country = self.country, sex = self.sex)
        diplom = diploma(thesis_advisor = "".join(thes_ad.name + " " + thes_ad.last_name),
                        specialty = random_spec_pos_resp.specialty,
                        graduation_year=self.day_of_birth(age=random_age, date_template=date_template, plus_years_to_birth=22))
        
        #=======Driver license data===============
        dr_lic = driverlicense(issue_date = self.day_of_birth(age=random_age, 
                            date_template=date_template, plus_years_to_birth=18), 
                            expiration_date = self.random_date(way="future", delta=[5,10]))
        
        #=======Biometrics data===============
        bio = biometric(sex = self.sex)    
        out_full = OutputModel(Personal_data = pers, Passport_data = pas, Address_data = ad,
                               Expirience_data = exp, Contacts_data = cont, Diploama_data = diplom,
                               Driver_license_data = dr_lic, Biometrics_data = bio)
        
        out = OutputModel(Personal_data = pers, Passport_data = pas)
        return out

