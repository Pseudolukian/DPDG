import data_structures.sql_models.base_sql_model as sql_model
from data_structures.sql_models.base_sql_model import SQLModel
from data_structures.file_models import SQL_buffer
from typing import Dict, Any
import json

from sqlmodel import create_engine, Session


class SQL_exporter:
    def __init__(self, db_name:str = "test", db_path:str = "./", 
                 user:str = None, password:str = None, sql_engine:str = "sqlite"):
        self.user = user
        self.password = password
        self.buffer = SQL_buffer()
        self.db_name = db_name
        self.db_path = db_path
        self.sql_engine = sql_engine
        self.all_models = {
        "persone": sql_model.persone,
        "address":sql_model.address,
        "biometric":sql_model.biometric,
        "contacts":sql_model.contacts,
        "diploma":sql_model.diploma,
        "driverlicense":sql_model.driverlicense,
        "expirience":sql_model.expirience,
        "passport":sql_model.passport
        }
    
    

    def dump_data(self, sql_buffer:SQL_buffer):
        DATABASE_URL = ""
        
        if self.sql_engine == "sqlite":
            DATABASE_URL = f"sqlite:///{self.db_path}{self.db_name}.db"
        elif self.sql_engine == "postgresql":
            DATABASE_URL = f"postgresql://{self.user}:{self.password}@localhost:5432/{self.db_name}"
        
        engine = create_engine(DATABASE_URL)
        pers_id = ""

        # Получаем уникальные имена классов из sql_buffer
        unique_model_names = {data.__class__.__name__ for data_set in sql_buffer for data in data_set}
        
        # Определение моделей для создания таблиц
        models_to_create = [self.all_models[name] for name in unique_model_names]
        # Создание только необходимых таблиц
        SQLModel.metadata.create_all(engine, tables=[model.__table__ for model in models_to_create])

        with Session(engine) as session:
            for data_set in sql_buffer:
                for data in data_set:
                    if data.__class__.__name__ in self.all_models:
                        if data.__class__.__name__ == "persone":
                            pers_id = data.personal_id
                        
                        model_class = self.all_models[data.__class__.__name__]
                        
                        data_dict = data.dict()

                        # Конвертирование списков и словарей в строки
                        for key, value in data_dict.items():
                            if isinstance(value, (list, dict)):
                                data_dict[key] = json.dumps(value)

                        # Присвоение to_personal_id, если необходимо
                        if 'to_personal_id' in model_class.__fields__:
                            data_dict['to_personal_id'] = pers_id
                        
                        db_instance = model_class(**data_dict)
                        session.add(db_instance)

            session.commit()
    
        