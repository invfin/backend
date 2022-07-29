from datetime import datetime

def more_than_month(last_date:datetime, most_recent_date:datetime = datetime.today()) -> bool:
    return (most_recent_date - last_date).days > 29
