from datetime import datetime

def format_date():
    current = datetime.now() 
    return current.strftime("%Y%m%d%H%M%S")