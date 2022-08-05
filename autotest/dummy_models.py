import random


class DummyModel:
    def __init__(self, model, quantity: int = 1, in_bulk: bool = False, *args, **kwargs):
        self.model = model
        # if not in_bulk:
        #     return self.create(model, quantity, *args, **kwargs)

    def create(self, model, quantity: int, *args, **kwargs):
        try:
            manager = model._default_manager
        except AttributeError:
            manager = model.objects
        for number in range(0, quantity):
            manager.create()

    def old_get_model_fields(self, model):
        return model._meta.fields

    def old_get_model_many_to_many(self, model):
        return model._meta.many_to_many

    def inspect_model(self):
        for field in self.get_model_fields():
            print('*'*100)
            self.inspect_model_field(field)

    def get_model_fields(self):
        return self.model._meta.get_fields()

    def inspect_model_field(self, field):
        field_info = field.__dict__
        print(field_info.keys())
        if "null" in field_info:
            print(field_info["null"])
