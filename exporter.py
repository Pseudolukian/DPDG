from models import OutputModel
from pathlib import Path
from uuid import uuid4
import pandas as pd
import json
from typing import Dict, Any
import openpyxl


class Exporter:
    
    def __init__(self, *args):
        self.data = args

    def dict(self) -> Dict[str, Any]:
        """
        Converts the provided models into a unified dictionary.

        This function aggregates attributes from all passed models into a single
        dictionary. The first model must contain a 'personal_id' attribute, which
        is used as the primary key for the resulting dictionary. All other attributes
        from all models are merged into the value of this primary key, excluding the
        'personal_id' itself.

        Returns:
            Dict[str, Any]: A dictionary where the key is the 'personal_id' of the first model
            and the value is a dictionary of attributes aggregated from all passed models.

        Raises:
            ValueError: If the first model doesn't have a 'personal_id' attribute.

        Example:
            If provided with models having attributes:
                - Model 1: personal_id: 'uuid1', name: 'John'
                - Model 2: passport_number: '123456'
            Result:
                {
                    'uuid4': {
                        'name': 'John',
                        'passport_number': '123456'
                    }
                }

        """
        uuid_key = getattr(self.data[0], 'personal_id', None)
        if not uuid_key:
            raise ValueError("Первая модель должна иметь атрибут personal_id!")

        out_data = {str(uuid_key): {}}
        for arg in self.data:
            out_data[str(uuid_key)].update(arg.dict(exclude={"personal_id"}, exclude_none=True))

        return out_data
    
    def json(self, path_json:Path = Path("./output.json")) -> str:
        out_data = self.dict()
        
        if path_json.exists():
            with open(path_json,"r") as file:
                existing_data = json.load(file)

            existing_data.update(out_data)
        
            with open(path_json,"w") as file:
                json.dump(existing_data, file, indent=4)
            
            return "JSON was opened and data was addeded."
        else:
            with open(path_json,"w") as file:
                json.dump(out_data, file, indent=4)
                return "JSON was created and data was addeded."
        
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
    
    def csv(self, path_csv:Path = Path("./output.csv")) -> str:
        out_data = self.dict()  # Directly calling the dict() method
        key = list(out_data.keys())[0]  # Getting the key (UUID)

        # Flattening the data and combining with UUID
        flattened_data = self._flatten_data(out_data[key])
        combined_data = {"personal_id": key, **flattened_data}

        # Transforming the dictionary to a DataFrame
        df = pd.DataFrame([combined_data])

        # Checking for file existence and appending/writing data accordingly
        if path_csv.exists():
            df.to_csv(path_csv, mode='a', header=False, index=False)
            return "Data was appended to existing CSV."
        else:
            df.to_csv(path_csv, mode='w', header=True, index=False)
            return "CSV was created and data was added."
    
    def xls(self, path_xls:Path = Path("./output.xlsx")) -> str:
        out_data = self.dict()  # Directly calling the dict() method
        key = list(out_data.keys())[0]  # Getting the key (UUID)

        # Flattening the data and combining with UUID
        flattened_data = self._flatten_data(out_data[key])
        combined_data = {"personal_id": key, **flattened_data}

        # Transforming the dictionary to a DataFrame
        df = pd.DataFrame([combined_data])

        if path_xls.exists():
            # Load existing workbook
            book = openpyxl.load_workbook(path_xls)
            writer = pd.ExcelWriter(path_xls, engine='openpyxl') 
            writer.book = book
            
            # Find the last row without data
            last_row = writer.book.active.max_row
            
            # Append the data without header
            df.to_excel(writer, index=False, header=False, startrow=last_row)

            writer.save()
            return "Data was appended to existing XLS."
        else:
            df.to_excel(path_xls, index=False)
            return "XLS was created and data was addeded."
        