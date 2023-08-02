from pydantic import BaseModel, root_validator, Field
import json
import random

from pathlib import Path
current_path = Path(__file__).parent
parent_directory = current_path.parent
json_path = parent_directory / "data_bases" / "contacts.json"

class contacts(BaseModel):
    """
    A model to represent and generate contact details for individuals.

    The `contacts` class provides a structured representation of various contact details for an individual.
    It generates a phone number, email address, nickname, and links to various social media accounts based on 
    predefined templates. Generated contact details can vary based on the given country and gender.

    Attributes:
        _country (str): Country of the contact. Defaults to "USA". Choices are ["USA", "RUSSIA", "UK"].
        _sex (str): Gender of the contact. Defaults to "M". Choices are ["M","F"].
        phone_number (str): Generated phone number for the contact.
        nick_name (str): Generated nickname for the contact.
        email (str): Generated email address for the contact.
        facebook_link (str): Generated Facebook profile link.
        vkontakte_link (str): Generated VKontakte profile link.
        LinkedIn_link (str): Generated LinkedIn profile link.
        Telegram_link (str): Generated Telegram profile link.

    Example:
        >>> contact_instance = contacts()
        >>> print(contact_instance.email)
        johndoe@email.com
        
    Note:
        Ensure you have the "contacts.json" file available and the appropriate data structures in it 
        to generate contact details seamlessly.
    """
    _country:str = Field(default="USA", choices=["USA", "RUSSIA", "UK"])
    _sex:str = Field(default="M", choices=["M","F"])
    phone_number:str = None
    nick_name:str = None
    email:str = None
    facebook_link:str = None
    vkontakte_link:str = None
    LinkedIn_link:str = None
    Telegram_link:str = None
    
    class Config:
        schema_extra = {
            "example": {
                "_country": "USA",
                "_sex": "M",
                "phone_number": "+1-123-456-7890",
                "nick_name": "john_doe",
                "email": "john_doe@email.com",
                "facebook_link": "https://facebook.com/john_doe",
                "vkontakte_link": "https://vk.com/john_doe",
                "LinkedIn_link": "https://linkedin.com/in/john_doe",
                "Telegram_link": "https://t.me/john_doe"
            }
        }
    
    @staticmethod
    def generate_phone_number(pattern: str) -> str:
        return ''.join(str(random.randint(0, 9)) if char == 'X' else char for char in pattern)
    
    @staticmethod
    def generate_nickname(prefix:str, body:str, postfix:str, devision:str) -> str:
        return ''.join(prefix + devision + body + devision + postfix)
    
    @property
    def country(self):
        return self._country
    @property
    def sex(self):
        return self._sex
    
    @root_validator(pre=True)
    def set_all_data(cls, values):
        contacts_data = json.load(open(json_path, "r"))
        values["phone_number"] = cls.generate_phone_number(contacts_data["phone_templates"][values["country"]])
        nick_pref = random.choice(contacts_data["NICK"][values["sex"]]["prefixes"])
        nick_body = random.choice(contacts_data["NICK"][values["sex"]]["bodys"])
        nick_postf = random.choice(contacts_data["NICK"][values["sex"]]["postfix"])
        devisions = random.choice(contacts_data["NICK"]["devisions"]  + [""])
        nick = cls.generate_nickname(prefix=nick_pref, body=nick_body, postfix=nick_postf, devision=devisions)
        values["nick_name"] = nick
        mail = random.choice(contacts_data["email_hosters"])
        values["email"] = "".join(nick + mail)
        for social_web in contacts_data["social_web_link_templates"]:
            for k,v in social_web.items():
                if k == "Facebook":   
                    values["facebook_link"] = "".join(v + nick)
                elif k == "VK":
                    values["vkontakte_link"] = "".join(v + nick)
                elif k == "LinkedIn":
                    values["LinkedIn_link"] = "".join(v + nick)
                elif k == "Telegram":
                    values["Telegram_link"] = "".join(v + nick)
        return values
    