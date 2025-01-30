"""
This is a utility module to generate realistic but fake data for various purposes.

Classes:
    - FakeGenerator:
        A main class to configure and generate various types of fake data.

        Attributes:
            - sex (List[str]): Gender options.
            - age (List[int]): Age range.
            - country (List[str]): Supported countries.
            - date_template (str): Format for date outputs.
            - generator (Generator): Inner utility for data component generation.

        Methods:
            - day_of_birth: Computes the date of birth given age.
            - random_date: Generates a random date.
            - rand_spec_pos_resp: Selects job attributes from a predefined database.

        Exceptions:
            Various ValueErrors based on input constraints.

    - Generator (Inner class of FakeGenerator):
        Utility class for generating individual data components.

        Attributes:
            - outer (FakeGenerator): Reference to outer instance.

        Methods:
            - personal: Generates fake personal data.
            - passport: Generates passport details.
            - diploma: Creates fake diploma data.
            - address: Returns address details.
            - contacts: Generates contact information.
            - biometric: Creates biometric details.
            - experience: Details of work experience.
            - driver_license: Generates driver's license details.

Imports:
    - data_structures.file_models: Required data structure models.
    - random: Randomization utilities.
    - datetime & dateutil.relativedelta: Date manipulation utilities.
    - json: For reading from JSON data sources.

Note:
    This module relies on predefined data sources and expects specific data structures.
    Always consult the docstring of each class/method for detailed information.

"""

from data_structures.file_models import *
import random
from random import randint
from typing import List
import json
from datetime import timedelta

from datetime import datetime
from dateutil.relativedelta import relativedelta

class FakeGenerator:
    """
    FakeGenerator: A utility class for generating realistic but fake data.

    Attributes:
        - sex (List[str]): A list containing genders ["M", "F"]. 
        - age (List[int]): A range of ages (e.g., [25, 70]).
        - country (List[str]): A list of countries. Supported countries are ["USA", "RUSSIA", "UK"].
        - date_template (str): The desired format of the dates.
        - generator (Generator): An instance of the inner `Generator` class for data generation.

    Methods:
        - day_of_birth: Computes the date of birth given the age and optionally additional years.
        - random_date: Generates a random date in the past or future based on the given delta.
        - rand_spec_pos_resp: Randomly selects a specialty, position, and responsibilities from the diploma JSON database.

    Exceptions:
        - Raises ValueError if the age range is not supported.
        - Raises ValueError if an unsupported gender or country is provided.
        - Raises ValueError if the date template is empty.
    """

    class Generator:
        """
        Generator: An inner utility class of FakeGenerator for generating individual data components.

        Attributes:
            - outer (FakeGenerator): Reference to the outer `FakeGenerator` instance for accessing its attributes and methods.

        Methods:
            - personal: Generates fake personal data.
            - passport: Generates fake passport data.
            - diploma: Generates fake diploma data.
            - address: Generates fake address data.
            - contacts: Generates fake contacts data.
            - biometric: Generates fake biometric data.
            - experience: Generates fake work experience data.
            - driver_license: Generates fake driver license data.
        """

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
        
    def __init__(self, sex:List[str] = ["M", "F"], 
                    age:List[int] = [25, 70], 
                    country:List[str] = ["USA", "RUSSIA", "UK"], 
                    date_template:str = "%m.%d.%Y",):
        """
        Initializes the FakeGenerator instance with provided or default values.

        Parameters:
            - sex (List[str], optional): A list containing gender options. Default is ["M", "F"].
            - age (List[int], optional): A range of ages. Default is [25, 70].
            - country (List[str], optional): A list of countries. Default is ["USA", "RUSSIA", "UK"].
            - date_template (str, optional): Format for date values. Default is "%m.%d.%Y".

        Exceptions:
            - Raises ValueError if provided values are out of supported range or format.
        """
        
        if age[0] < 24:
            raise ValueError('The first age value must be at least 24.')
        if age[1] > 70:
            raise ValueError('The second age value must not exceed 70.')
        
        for s in sex:
            if s not in ["M", "F"]:
                raise ValueError('The sex value must be either "M" or "F".')
        
        for c in country:
            if c not in ["USA", "RUSSIA", "UK"]:
                raise ValueError('The country value must be either "USA", "RUSSIA" or "UK".')    
            
        if len(date_template) == 0:
            raise ValueError('The date template coud not be empty!')
        
        self.sex = random.choice(sex)
        self.age = age
        self.country = random.choice(country)
        self.generator = self.Generator(self)
        self.date_template = date_template   
        self._random_age = randint(self.age[0], self.age[1])  
    
         
    
    def day_of_birth(self, age: int, plus_years_to_birth:int = 0) -> str:
        """
        Computes the date of birth given an age and optionally additional years.

        Parameters:
            - age (int): The age of the individual.
            - plus_years_to_birth (int, optional): Number of years to add to the birthdate.

        Returns:
            - str: The computed date in the format specified by `date_template`.
        """
        current_date = datetime.now()
        
        # Вычисляем год рождения
        year_of_birth = current_date.year - age + plus_years_to_birth
        
        # Генерируем случайный месяц
        random_month = random.randint(1, 12)

        # Генерируем случайный день с учетом того, какой месяц
        if random_month == 2:  # Февраль
            if (year_of_birth % 4 == 0 and year_of_birth % 100 != 0) or (year_of_birth % 400 == 0):
                random_day = random.randint(1, 29)  # Високосный год
            else:
                random_day = random.randint(1, 28)  # Невисокосный год
        elif random_month in [4, 6, 9, 11]:  # Месяцы с 30 днями
            random_day = random.randint(1, 30)
        else:  # Остальные месяцы
            random_day = random.randint(1, 31)

        # Создаем дату рождения
        date_of_birth = datetime(year=year_of_birth, month=random_month, day=random_day)

        return date_of_birth.strftime(self.date_template)
    
    def random_date(self, way: str = "past", delta: List[int] = [1, 20]) -> str:
        """
        Generates a random date based on the specified range and direction (past/future).

        Parameters:
            - way (str, optional): Direction for date generation - "past" or "future". Default is "past".
            - delta (List[int], optional): Range for random date generation. Default is [1, 20].

        Returns:
            - str: The generated date in the format specified by `date_template`.

        Exceptions:
         - Raises ValueError if an unsupported value for 'way' is provided.
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
        Randomly selects job attributes from a predefined diploma JSON database.

        Returns:
            - job_specs: An instance of the `job_specs` model with randomly populated fields.
        """
        specs_out = job_specs()
        with open("./data_structures/data_bases/diploma.json", "r") as file:
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
    
    
    

