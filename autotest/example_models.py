import uuid
import os
import random
import string

from autotest.exceptions import ArgsAndKwargsExcpetion


class ExampleModel:
    def __init__(
        self,
        model,
        quantity: int = 1,
        in_bulk: bool = False,
        full_null: bool = True,
        *args,
        **kwargs
    ):
        if args and kwargs:
            raise ArgsAndKwargsExcpetion()
        return self.inspect_model_field(model)
        # if not in_bulk:
        #     return self.create(model, quantity, *args, **kwargs)

    def create(self, model, quantity: int, *args, **kwargs):
        try:
            manager = model._default_manager
        except AttributeError:
            manager = model.objects
        for number in range(quantity):
            manager.create()

    def old_get_model_fields(self, model):
        return model._meta.fields

    def old_get_model_many_to_many(self, model):
        return model._meta.many_to_many

    def inspect_model(self, model):
        for field in self.get_model_fields(model):
            print('*'*100)
            print(field)
            print('*' * 100)
            self.inspect_model_field(field)

    def get_model_fields(self, model):
        return model._meta.get_fields()

    def generate_random_data(self, field_type, min_value: int = 1, max_value: int = 1000):
        data_generator = {

        }

        return data_generator[field_type]

    def create_random_string(self, min_value: int = 1, max_value: int = 1000):
        characters = string.ascii_letters + string.digits + string.punctuation
        number = random.randint(min_value, max_value)
        return ''.join(random.choice(characters) for _ in range(number))

    def create_random_slug(self, max_value: int = 1000):
        return str(uuid.UUID(bytes=os.urandom(max_value), version=4))

    def create_random_number(self, min_value: int = 1, max_value: int = 1000):
        return random.randint(min_value, max_value)
        # random.shuffle([index for index in range(number)])

    def inspect_model_field(self, field):
        field_info = field.__dict__
        field_type = field.get_internal_type()
        if "related_model" in field_info:
            self.inspect_model(field_info["related_model"])

