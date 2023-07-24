from models import OutputModel
from pathlib import Path
from uuid import uuid4
import pandas as pd
import json
from typing import Dict, Any


class Exporter:
    
    def __init__(self, data:OutputModel):
        self.data = data

    def dict(self) -> Dict[str, Any]:
        out_data = self.data.dict(exclude_none = True)
        return out_data
    
    def json(self, path_json:Path = Path("./output.json")) -> str:
        out_data = self.data.dict(exclude_none = True)
        pers_id = str(uuid4())
        prep_json_data = {}
        prep_json_data[pers_id] = out_data
        
        if path_json.exists():
            with open(path_json,"r") as file:
                existing_data = json.load(file)

            existing_data.update(prep_json_data)
        
            with open(path_json,"w") as file:
                json.dump(existing_data, file, indent=4)
            
            return "JSON was opened and data was addeded."
        else:
            with open(path_json,"w") as file:
                json.dump(prep_json_data, file, indent=4)
                return "JSON was created and data was addeded."
        
    def _flatten_data(self, data):
        flat_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    flat_data[subkey] = subvalue  # Убираем название модели из ключа
            else:
                flat_data[key] = value
        return flat_data
    
    def csv(self, path_csv:Path = Path("./output.csv")) -> str:
        out_data = self.data.dict(exclude_none=True)
        flattened_data = self._flatten_data(out_data)

        # Добавление UUID
        personal_id = {"personal_id": str(uuid4())}
        
        # Объединение personal_id и flattened_data
        combined_data = {**personal_id, **flattened_data}
        
        # Преобразование словаря в DataFrame
        df = pd.DataFrame([combined_data])

        # Проверка на наличие файла и дозапись данных, если файл существует
        if path_csv.exists():
            df.to_csv(path_csv, mode='a', header=False, index=False)
            return "Data was appended to existing CSV."
        else:
            df.to_csv(path_csv, mode='w', header=True, index=False)
            return "CSV was created and data was addeded."
    
    def xls(self, path_xls:Path = Path("./output.xlsx")) -> str:
        out_data = self.data.dict(exclude_none=True)
        flattened_data = self._flatten_data(out_data)
        personal_id = {"personal_id": str(uuid4())}
        combined_data = {**personal_id, **flattened_data}
        

        df = pd.DataFrame([combined_data])

        if path_xls.exists():
            book = pd.read_excel(path_xls, engine='openpyxl')
            writer = pd.ExcelWriter(path_xls, engine='openpyxl')
            writer.book = book
            df.to_excel(writer, startrow=writer.sheets['Sheet1'].max_row, index = False, header = False)
            writer.save()
            return "Data was appended to existing XLS."
        else:
            df.to_excel(path_xls, index=False)
            return "XLS was created and data was addeded."    
        