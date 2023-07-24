from datetime import datetime, timedelta
import random
from typing import List
import json

def random_date(way: str = "past", delta: List[int] = [1, 20], template:str = '%d.%M.%Y') -> str:
    current_date = datetime.now()
    years_delta = random.randint(delta[0], delta[1])
    
    if way == "past":
        random_date_result = current_date - timedelta(days=365.25 * years_delta)
    elif way == "future":
        random_date_result = current_date + timedelta(days=365.25 * years_delta)
    else:
        raise ValueError(f"Invalid value for 'way': {way}. Use 'past' or 'future'.")
    
    return random_date_result.strftime(template)



