from .create_data import DataCreator
from ..example_models.exceptions import ArgsAndKwargsExcpetion


class ExampleModel(DataCreator):
    def __init__(
        self,
        model,
        quantity: int = 1,
        in_bulk: bool = False,
        full_null_fields: bool = True,
        *args,
        **kwargs
    ):
        if args and kwargs:
            raise ArgsAndKwargsExcpetion()
        return self.inspect_model(model)
        # if not in_bulk:
        #     return self.create(model, quantity, *args, **kwargs)

    # def create(self, model, quantity: int, *args, **kwargs):

    #     for number in range(quantity):
    #         manager.create()

    def create_model(self, model: type) -> type:
        try:
            manager = model._default_manager
        except AttributeError:
            manager = model.objects
        finally:
            return manager.create(**self.inspect_model(model))

    def inspect_model(self, model: type) -> dict:
        fields_info = dict()
        for field in model._meta.get_fields():
            fields_info.update(self.inspect_field(field))
        return fields_info

    def inspect_field(self, field: type) -> dict:
        field_info = field.__dict__
        field_type = field.get_internal_type()
        return {field.name: self.generate_random_data_per_field(field_type, field)}
        #if "related_model" in field_info:
         #   self.inspect_model(field_info["related_model"])

    def generate_random_data_per_field(
        self,
        field_type: str,
        field,
        min_value: int = 1,
        max_value: int = 1000
    ):
        data_generator = {
            "DateTimeField": ExampleModel.create_random_datetime(),
            "DateField": ExampleModel.create_random_date(),
            "TimeField": ExampleModel.create_random_hour(),

            # "DurationField": ExampleModel.create(),

            # "AutoField": ExampleModel.create(),
            # "BigAutoField": ExampleModel.create(),
            # "SmallAutoField": ExampleModel.create(),

            # "BinaryField": ExampleModel.create(),
            # "CommaSeparatedIntegerField": ExampleModel.create(),

            "DecimalField": ExampleModel.create_random_float(),
            "FloatField": ExampleModel.create_random_float(),

            "BigIntegerField": ExampleModel.create_random_integer(min_value=10000),
            "PositiveBigIntegerField": ExampleModel.create_random_positive_integer(min_value=10000),
            "PositiveIntegerField": ExampleModel.create_random_positive_integer(),
            "PositiveSmallIntegerField": ExampleModel.create_random_positive_integer(max_value=10000),
            "IntegerField": ExampleModel.create_random_integer(),
            "SmallIntegerField": ExampleModel.create_random_integer(max_value=10000),

            "CharField": ExampleModel.create_random_string(),
            "TextField": ExampleModel.create_random_string(),

            "SlugField": ExampleModel.create_random_slug(),

            # "URLField": ExampleModel.create(),
            # "UUIDField": ExampleModel.create(),
            # "EmailField": ExampleModel.create(),

            # "Empty": ExampleModel.create(),
            # "Field": ExampleModel.create(),
            # "NOT_PROVIDED": ExampleModel.create(),

            # "FilePathField": ExampleModel.create(),
            # "FileField": ExampleModel.alg(),
            # "ImageField": ExampleModel.alg(),
            # "JSONField": ExampleModel.alg(),

            # "GenericIPAddressField": ExampleModel.create(),
            # "IPAddressField": ExampleModel.create(),

            "BooleanField": ExampleModel.create_random_bool(),
            "NullBooleanField": ExampleModel.create_random_bool(),

            "ForeignKey": ExampleModel.create_model(field.related_model),
            "OneToOneField": ExampleModel.create_model(field.related_model),
            # "ManyToManyField": ExampleModel.alg(),
        }

        return data_generator[field_type]


