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

        characters = string.ascii_letters
        if use_digits:
            characters += string.digits
        if use_punctuation:
            characters += string.punctuation

        number = random.randint(10, max_value)
        return "".join(random.choice(characters) for _ in range(number))

    @staticmethod
    def create_random_text(max_value: int = 1000):
        return textwrap.wrap(LOREM_TEXT, max_value)[0]

    @staticmethod
    def create_random_bool() -> bool:
        return bool(random.randint(0, 1) == 1)

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
    def create_random_url(max_value: int = 100, secure = True):
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
