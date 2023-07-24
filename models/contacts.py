from pydantic import BaseModel, root_validator, Field
import json
import random

class contacts(BaseModel):
    _country:str = Field(default="USA", choices=["USA", "RUSSIA", "UK"])
    _sex:str = Field(default="M", choices=["M","F"])
    phone_number:str = None
    nick_name:str = None
    email:str = None
    facebook_link:str = None
    vkontakte_link:str = None
    LinkedIn_link:str = None
    Telegram_link:str = None
    
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
        contacts_data = json.load(open("./data_structures/contacts.json", "r"))
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
            
        
        
        
    