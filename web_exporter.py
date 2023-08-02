from data_structures.file_models.buffer import Buffer
from typing import List

class Web_exporter:
    
    def _flatten_data(self, data: dict, parent_key='', sep='_') -> dict:
        flat_data = {}
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):
                flat_data.update(self._flatten_data(value, new_key, sep=sep))
            else:
                flat_data[new_key] = value
        return flat_data
    
    def buffer_to_flat_json(self, buffer: Buffer) -> List[dict]:
        flat_list = []
        for item in buffer:
            flat_list.append(self._flatten_data(item.dict()))
        return flat_list