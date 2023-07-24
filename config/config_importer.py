import json

def importer(config_path:str = "./config/conf.json", conf_key = "date_format") -> str:
    config_data = json.load(open(config_path,'r'))
    return config_data[conf_key]