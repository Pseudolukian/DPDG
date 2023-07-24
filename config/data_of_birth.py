from datetime import datetime
from dateutil.relativedelta import relativedelta

def day_of_birth(age: int, date_template: str, plus_years_to_birth:int = 0) -> str:
    date_now = datetime.now()
    date_of_birth = date_now - relativedelta(years=age)
    date_with_added_years = date_of_birth + relativedelta(years=plus_years_to_birth)
    return date_with_added_years.strftime(date_template)