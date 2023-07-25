from models import *
import random
from random import randint
from typing import List
import json
from datetime import timedelta

from datetime import datetime
from dateutil.relativedelta import relativedelta



class FakeGenerator:
    
    class Generator:
        def __init__(self, outer_instance):
            self.outer = outer_instance

        def personal(self) -> persone:
            
            pers = persone(country = self.outer.country, sex = self.outer.sex, age = self.outer._random_age)
            return pers

        def passport(self) -> passport:
            
            pas = passport(country = self.outer.country, sex = self.outer.sex,
                           date_of_birth = self.outer.day_of_birth(age = self.outer._random_age),
                           issue_date = self.outer.day_of_birth(age=self.outer._random_age, plus_years_to_birth=16),
                           expiration_date = self.outer.day_of_birth(age=self.outer._random_age, plus_years_to_birth=56))
            return pas

        def diploma(self) -> diploma:
            
            random_spec_pos_resp = self.outer.rand_spec_pos_resp()
            thes_ad = persone(country=self.outer.country, sex=self.outer.sex)
            diplom = diploma(thesis_advisor="".join(thes_ad.name + " " + thes_ad.last_name),
                            specialty=random_spec_pos_resp.specialty,
                            graduation_year=self.outer.day_of_birth(age=self.outer._random_age, plus_years_to_birth=22))
            return diplom
        
        def address(self) -> address:
            return address(country=self.outer.country)
        
        def contacts(self) -> contacts:
            return contacts(country=self.outer.country, sex=self.outer.sex)

        def biometric(self) -> biometric:
            return biometric(sex=self.outer.sex)
        
        def experience(self) -> expirience:
            random_spec_pos_resp = self.outer.rand_spec_pos_resp()
            cur_job_start = self.outer.random_date(way="past", delta=[1,3])
            prev_job_start = self.outer.random_date(way="past", delta=[3,5])
            supervisor = persone(country=self.outer.country, sex=self.outer.sex)
            exp = expirience(country=self.outer.country, 
                             cur_position=random_spec_pos_resp.position,
                             responsibilities=random_spec_pos_resp.responsibilities,
                             cur_comp_start_date=cur_job_start,
                             supervisor_name="".join(supervisor.name + " " + supervisor.last_name),
                             prev_position=self.outer.rand_spec_pos_resp().position,
                             prev_comp_start_date=prev_job_start)
            return exp

        
        def driver_license(self) -> driverlicense:
            
            dr_lic = driverlicense(issue_date=self.outer.day_of_birth(age = self.outer._random_age, plus_years_to_birth=18), 
                                   expiration_date=self.outer.random_date(way="future", delta=[5,10]))
            return dr_lic
        
    def __init__(self,sex:str = "M", age:List[int] = [25,70], 
                 country:str = "USA", date_template:str = "%m.%d.%Y",):
        self.sex = sex
        self.age = age
        self.country = country
        self.generator = self.Generator(self)
        self.date_template = date_template   
        self._random_age = randint(self.age[0], self.age[1])
    
    def day_of_birth(self, age: int, plus_years_to_birth:int = 0) -> str:
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
        current_date = datetime.now()
        date_of_birth = current_date - relativedelta(years = age)
        date_with_added_years = date_of_birth + relativedelta(years=plus_years_to_birth)
        return date_with_added_years.strftime(self.date_template)
    
    def random_date(self, way: str = "past", delta: List[int] = [1, 20]) -> str:
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
        
        return random_date_result.strftime(self.date_template)
    
        
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
    
    
    

