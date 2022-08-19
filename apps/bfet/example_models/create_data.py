from typing import Dict

import uuid
import random
import string
import datetime
import textwrap

from .constants import LIST_EMAIL_DOMAINS, LOREM_TEXT

class DataCreator:
    @staticmethod
    def create_random_string(
        max_value: int = 800,
        use_punctuation: bool = False,
        use_digits: bool = True
    ):
        min_value = 10
        characters = string.ascii_letters
        if use_digits:
            characters += string.digits
        if use_punctuation:
            characters += string.punctuation
        if max_value < min_value:
            min_value += max_value - min_value
        number = random.randint(min_value, max_value)
        return "".join(random.choice(characters) for _ in range(number))

    @staticmethod
    def create_random_text(max_value: int = 1000):
        return textwrap.wrap(LOREM_TEXT, max_value)[0]

    @staticmethod
    def create_random_bool() -> bool:
        return bool(random.randint(0, 1) == 1)

    @staticmethod
    def create_random_json() -> Dict:
        random_dict = {}
        choices = {
            1: DataCreator.create_random_string(),
            2: DataCreator.create_random_bool(),
            3: DataCreator.create_random_datetime().strftime("%m/%d/%Y, %H:%M:%S"),
            4: DataCreator.create_random_float(),
        }
        for index in range(3):
            key = random.randint(1, 4)
            value = random.randint(1, 4)
            key = choices[key]
            value = choices[value]
            random_dict[f"{key}"] = value
        return random_dict

    @staticmethod
    def create_random_slug(max_value: int = 800, use_digits: bool = True):
        return "-".join(
            [
                DataCreator.create_random_string(3, 10, False, use_digits) for _ in range(4)
            ]
        )[:max_value]


    @staticmethod
    def create_random_email(max_value: int = 25):
        email_name = DataCreator.create_random_string(max_value)
        email_domain = random.choice(LIST_EMAIL_DOMAINS)
        return f"{email_name}@{email_domain}"

    @staticmethod
    def create_random_url(max_value: int = 100, secure=True):
        domain = DataCreator.create_random_string(max_value)
        top_level_domain = random.choice(LIST_EMAIL_DOMAINS).split(".")[-1]
        protocol = "https" if secure else "http"
        return f"{protocol}://{domain}.{top_level_domain}"

    @staticmethod
    def create_random_uuid(kind: int = 4, **kwargs):
        uuids = {
            1: uuid.uuid1,
            3: uuid.uuid3,
            4: uuid.uuid4,
            5: uuid.uuid5
        }
        return uuids[kind](**kwargs)

    @staticmethod
    def create_random_date(day: int = None, month: int = None, year: int = None):
        month = month if month else random.randint(1, 12)
        if month == 2:
            max_day = 28
        elif month in [1, 3, 5, 7, 8, 10, 12]:
            max_day = 31
        else:
            max_day = 30
        day = day if day else random.randint(1, max_day)
        year = year if year else random.randint(1900, 2100)
        return datetime.date(year=year, month=month, day=day)

    @staticmethod
    def create_random_hour(hour: int = None, minute: int = None, second: int = None):
        hour = hour if hour else random.randint(0, 23)
        minute = minute if minute else random.randint(0, 59)
        second = second if second else random.randint(0, 59)
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
        if max_value < min_value:
            min_value += max_value - min_value
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
        if max_value < min_value:
            min_value += max_value - min_value
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
