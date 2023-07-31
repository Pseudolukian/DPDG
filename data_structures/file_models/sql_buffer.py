from pydantic import BaseModel
from typing import List
from data_structures.file_models import OutputModel

class SQL_buffer(BaseModel):
    buf: List[List[OutputModel]] = []
    
    def add(self, *data: OutputModel):
        self.buf.append(list(data))