"""
A module designed to manage and export data from an SQL buffer into various SQL databases such as SQLite and PostgreSQL.

Imports:
    - Various SQL models and utilities.
    - SQLModel for database operations.
    - JSON for data serialization.

Classes:
    - SQL_exporter:
        Manages the process of exporting data from the SQL buffer to the desired SQL database.

Dependencies:
    Requires SQLModel for ORM-related operations.
"""


import data_structures.sql_models.base_sql_model as sql_model
from data_structures.sql_models.base_sql_model import SQLModel
from data_structures.file_models import SQL_buffer
import json

from sqlmodel import create_engine, Session


class SQL_exporter:
    """  
    Manages the process of exporting data from the SQL buffer to the desired SQL database.

    Attributes:
        - user (str): Username for the SQL database. 
        - password (str): Password for the SQL database.
        - buffer (SQL_buffer): Buffer instance which holds the SQL data.
        - db_name (str): Name of the database.
        - db_path (str): Path to the database.
        - sql_engine (str): Type of the SQL engine (sqlite or postgresql).
        - all_models (dict): Dictionary containing references to all SQL model classes.

    Methods:
        - dump_data(sql_buffer:SQL_buffer): Exports the data from the SQL buffer to the selected SQL database.
    """
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
        """
        Exports the data from the SQL buffer to the selected SQL database.

        Parameters:
            - sql_buffer (SQL_buffer): The buffer instance containing the SQL data to be exported.

        Notes:
            The method creates appropriate tables in the database if they don't exist and populates them with the data from the buffer.
        """
        DATABASE_URL = ""
        
        if self.sql_engine == "sqlite":
            DATABASE_URL = f"sqlite:///{self.db_path}{self.db_name}.db"
        elif self.sql_engine == "postgresql":
            DATABASE_URL = f"postgresql://{self.user}:{self.password}@localhost:5432/{self.db_name}"
        
        engine = create_engine(DATABASE_URL)
        pers_id = ""

        
        unique_model_names = {data.__class__.__name__ for data_set in sql_buffer for data in data_set}
        
        
        models_to_create = [self.all_models[name] for name in unique_model_names]
        SQLModel.metadata.create_all(engine, tables=[model.__table__ for model in models_to_create])

        with Session(engine) as session:
            for data_set in sql_buffer:
                for data in data_set:
                    if data.__class__.__name__ in self.all_models:
                        if data.__class__.__name__ == "persone":
                            pers_id = data.personal_id
                        
                        model_class = self.all_models[data.__class__.__name__]
                        
                        data_dict = data.dict()

                        for key, value in data_dict.items():
                            if isinstance(value, (list, dict)):
                                data_dict[key] = json.dumps(value)

                        if 'to_personal_id' in model_class.__fields__:
                            data_dict['to_personal_id'] = pers_id
                        
                        db_instance = model_class(**data_dict)
                        session.add(db_instance)

            session.commit()
    
        