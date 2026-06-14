from datetime import date

def compare_to_date(current: date) -> bool:    
    return current < date.today()