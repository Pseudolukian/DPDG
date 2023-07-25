from models import OutputModel, Buffer
from pathlib import Path
from uuid import uuid4
import pandas as pd
import json
from typing import Dict, Any
import openpyxl


class Exporter:
        
    def __init__(self):
        self.buffer = Buffer()
            

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

    
    def json(self, path_json: Path = Path("./output.json")) -> str:
        out_data = self.dict()
        
        if path_json.exists():
            with open(path_json, "r") as file:
                existing_data = json.load(file)

                # Проверка, что существующие данные являются списком
                if not isinstance(existing_data, list):
                    return "Error: Existing JSON data is not a list format."

                # Добавление новых данных в существующий список
                existing_data.extend(out_data)
            
            with open(path_json, "w") as file:
                json.dump(existing_data, file, indent=4)
            
            return "JSON was opened and data was added."
        
        else:
            with open(path_json, "w") as file:
                json.dump(out_data, file, indent=4)
            
            return "JSON was created and data was added."

        
    def _flatten_data(self, data: dict) -> dict:
        """Flattens nested dictionaries into a single-level dictionary."""
        flat_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    flat_data[subkey] = subvalue  # Убираем название модели из ключа
            else:
                flat_data[key] = value
        return flat_data

    def csv(self, path_csv: Path = Path("./output.csv")) -> str:
        out_data_list = self.dict()  # Directly calling the dict() method

        rows = []  # This will hold all the data rows

        for data_dict in out_data_list:
            key = list(data_dict.keys())[0]  # Getting the key (UUID)
            # Flattening the data and combining with UUID
            flattened_data = self._flatten_data(data_dict[key])
            combined_data = {"personal_id": key, **flattened_data}
            rows.append(combined_data)

        # Transforming the dictionary list to a DataFrame
        df = pd.DataFrame(rows)

        # Checking for file existence and appending/writing data accordingly
        if path_csv.exists():
            df.to_csv(path_csv, mode='a', header=False, index=False)
            return "Data was appended to existing CSV."
        else:
            df.to_csv(path_csv, mode='w', header=True, index=False)
            return "CSV was created and data was added."

    def xls(self, path_xls: Path = Path("./output.xlsx")) -> str:
        out_data = self.dict()  # Получение данных

        # Преобразование словаря данных в DataFrame
        flattened_data_list = [self._flatten_data(data) for data in out_data]
        df_new = pd.DataFrame(flattened_data_list)

        # Проверка существования файла и запись данных соответственно
        if path_xls.exists():
            # Если файл существует, читаем его содержимое
            xls = pd.ExcelFile(path_xls)
            # Предполагаем, что данные нужно добавить в первый лист
            sheet_name = xls.sheet_names[0]
            df_old = xls.parse(sheet_name)
            
            # Конкатенация старых и новых данных
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            
            # Запись объединенного DataFrame обратно в XLS
            with pd.ExcelWriter(path_xls, engine='xlsxwriter') as writer:
                df_combined.to_excel(writer, sheet_name=sheet_name, index=False)
            
            return "Data was appended to the existing XLS sheet."
        else:
            df_new.to_excel(path_xls, sheet_name="Sheet1", index=False)
            return "XLS was created and data was added."
