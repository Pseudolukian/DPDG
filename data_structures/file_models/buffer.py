from pydantic import BaseModel
from typing import List,Type
from data_structures.file_models import OutputModel

class Buffer(BaseModel):
    """
    A buffer to hold a collection of Pydantic models for subsequent data export.

    The `Buffer` class is designed to temporarily store Pydantic models, primarily of type `OutputModel`. 
    Once these models are accumulated in the buffer, they can be efficiently processed by other functions 
    or methods to export the contained data into various formats such as JSON, CSV, or XLS.

    Attributes:
        buf (List[OutputModel]): A list holding instances of `OutputModel`. Defaults to an empty list.

    Methods:
        add(*data: Type[OutputModel]): Adds one or more `OutputModel` instances to the buffer.

    Example:
        >>> f_exp = File_Exporter()
        >>> f_g = FakeGenerator()
        >>> pers = f_g.generator.personal()
        >>> f_exp.buffer.add(pers)
        >>> print(f_exp.buffer.buf)
        [persone(personal_id=UUID('325fa848-fe6a-46d9-a732-a9e7070d95cc'), name='Daniel', last_name='Martin', age=39)]

    Note:
        Ensure that the models added to the buffer are compatible with the export functions 
        that you plan to use later for a seamless export experience.
    """
    buf:List[OutputModel] = []
    
    
    def add(self, *data: Type[OutputModel]):
        for item in data:
            self.buf.append(item)