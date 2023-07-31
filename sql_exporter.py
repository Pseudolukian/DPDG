import data_structures.sql_models.base_sql_model as sql_model
from data_structures.sql_models.base_sql_model import SQLModel
from data_structures.file_models import SQL_buffer
from typing import Dict, Any

from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker


class SQL_exporter:
    def __init__(self, bd_name:str = "test", db_path:str = "./", user:str = None, password:str = None):
        self.user = user
        self.password = password
        self.buffer = SQL_buffer()
        self.db_name = bd_name
        self.db_path = db_path
    
    def dict(self) -> Dict[str, Any]:
        if not self.buffer.buf:  # If buffer is empty
            return {}

        out_data_list = []

        # Use a temporary buffer to hold current models 
        temp_buffer = []

        for arg in self.buffer.buf:
            # If we found a personal_id model, create a new record and add to out_data_list
            if hasattr(arg, 'personal_id'):
                if temp_buffer:
                    single_record = {}
                    uuid_key = getattr(temp_buffer[0], 'personal_id')
                    single_record[str(uuid_key)] = temp_buffer[0].dict(exclude={"personal_id"}, exclude_none=True)
                    for model in temp_buffer[1:]:
                        single_record[str(uuid_key)].update(model.dict(exclude_none=True))
                    out_data_list.append(single_record)
                    temp_buffer = []

                temp_buffer.append(arg)
            else:
                temp_buffer.append(arg)

        # Handle the last set of models in the buffer
        if temp_buffer:
            single_record = {}
            uuid_key = getattr(temp_buffer[0], 'personal_id')
            single_record[str(uuid_key)] = temp_buffer[0].dict(exclude={"personal_id"}, exclude_none=True)
            for model in temp_buffer[1:]:
                single_record[str(uuid_key)].update(model.dict(exclude_none=True))
            out_data_list.append(single_record)

        return out_data_list
    
    def lsql_cr_tables(self, sql_buffer:SQL_buffer):
        DATABASE_URL = f"sqlite:///{self.db_path}{self.db_name}.db"
        engine = create_engine(DATABASE_URL)
        
        model_names = {item.__class__.__name__ for item in sql_buffer[0]}
        
        all_models = {
        "persone": sql_model.persone,
        "address":sql_model.address,
        "biometric":sql_model.biometric,
        "contacts":sql_model.contacts,
        "diploma":sql_model.diploma,
        "driverlicense":sql_model.driverlicense,
        "expirience":sql_model.expirience,
        "passport":sql_model.passport
        }
        
        models_to_create = [all_models[name] for name in model_names if name in all_models]
        
        for model in models_to_create:
            if issubclass(model, SQLModel):
                model.__table__.create(bind=engine, checkfirst=True)
    
    def lsql_dump_data(self, sql_buffer:SQL_buffer):
            
        all_models = {
            "persone": sql_model.persone,
            "address": sql_model.address,
            "biometric": sql_model.biometric,
            "contacts": sql_model.contacts,
            "diploma": sql_model.diploma,
            "driverlicense": sql_model.driverlicense,
            "expirience": sql_model.expirience,
            "passport": sql_model.passport
        }

        
        for set in sql_buffer:
            for model in set:
                if model.__class__.__name__ in all_models:
                    mod_to_dump = all_models[model.__class__.__name__]
                    mod_to_dump()
                    print(mod_to_dump)
                
        