import uuid
import os
import random
import string
import datetime


class DataCreator:
    @staticmethod
    def create_random_string(min_value: int = 1, max_value: int = 1000):
        characters = string.ascii_letters + string.digits + string.punctuation
        number = random.randint(min_value, max_value)
        return ''.join(random.choice(characters) for _ in range(number))

    @staticmethod
    def create_random_bool() -> bool:
        return bool(random.randint(0, 1) == 1)

    @staticmethod
    def create_random_slug(max_value: int = 1000):
        return str(uuid.UUID(bytes=os.urandom(max_value), version=4))

    @staticmethod
    def create_random_date(day: int = None, month: int = None, year: int = None):
        day = day if day else random.randint(1, 30)
        month = month if month else random.randint(1, 12)
        year = year if year else random.randint(1900, 2100)
        return datetime.date(year=year, month=month, day=day)

    @staticmethod
    def create_random_hour(hour: int = None, minute: int = None, second: int = None):
        hour = hour if hour else random.randint(0, 24)
        minute = minute if minute else random.randint(0, 60)
        second = second if second else random.randint(0, 60)
        return datetime.time(hour, minute, second)

    @staticmethod
    def create_random_datetime(
        day: int = None,
        month: int = None,
        year: int = None,
        hour: int = None,
        minute: int = None,
        second: int = None,
    ):
        date = DataCreator.create_random_date(day, month, year)
        time = DataCreator.create_random_hour(hour, minute, second)
        return datetime.datetime.combine(date, time)

    @staticmethod
    def create_random_integer(min_value: int = 0, max_value: int = 10000000):
        fnct = random.choice(
            [DataCreator.create_random_negative_integer, DataCreator.create_random_positive_integer]
        )
        return fnct(min_value, max_value)

    @staticmethod
    def create_random_negative_integer(min_value: int = 0, max_value: int = 10000000):
        return (random.randint(min_value, max_value) * -1)

    @staticmethod
    def create_random_positive_integer(min_value: int = 0, max_value: int = 10000000):
        return random.randint(min_value, max_value)

    @staticmethod
    def create_random_float(min_value: float = 0, max_value: float = 10000000, after_coma: int = 2):
        fnct = random.choice(
            [DataCreator.create_random_negative_float, DataCreator.create_random_positive_float]
        )
        return fnct(min_value, max_value, after_coma)

    @staticmethod
    def create_random_positive_float(min_value: float = 0, max_value: float = 10000000, after_coma: int = 2):
        return round(random.uniform(min_value, max_value), after_coma)

    @staticmethod
    def create_random_negative_float(min_value: float = 0, max_value: float = 10000000, after_coma: int = 2):
        return (round(random.uniform(min_value, max_value), after_coma) * -1)
