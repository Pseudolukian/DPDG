from pydantic import BaseModel
from typing import List,Type
from data_structures.file_models import OutputModel

class Buffer(BaseModel):
    buf:List[OutputModel] = []
    
    
    def add(self, *data: Type[OutputModel]):
        for item in data:
            self.buf.append(item)