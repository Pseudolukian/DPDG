from pydantic import BaseModel
from typing import List
from data_structures.file_models import OutputModel

class SQL_buffer(BaseModel):
    """
    A buffer model designed to hold and manage a list of OutputModel instances.
    
    SQL_buffer is primarily used to store OutputModel data in a structured manner before
    transferring the data to an SQL database or processing it further. The buffer can 
    hold a list of lists containing OutputModel instances.
    
    Attributes:
    - buf (List[List[OutputModel]]): A list of lists, where each inner list contains OutputModel instances.
    
    Methods:
    - add: Adds OutputModel instances to the buffer.
    """
    buf: List[List[OutputModel]] = []
    
    class Config:
        schema_extra = {
            "example": {
                "buf": [
                    [
                        {
                            "Personal_data": {
                                "personal_id": "65685aba-97cd-4a72-9535-6a302bf56715",
                                "_sex": "M",
                                "_country": "USA",
                                "name": "John",
                                "last_name": "Doe",
                                "age": 30
                            }
                        }
                    ]
                ]
            }
        }
    
    def add(self, *data: OutputModel):
        """ 
        Adds provided OutputModel instances to the buffer.
        
        Args:
        - *data (OutputModel): Variable length argument list of OutputModel instances.
        """
        self.buf.append(list(data))