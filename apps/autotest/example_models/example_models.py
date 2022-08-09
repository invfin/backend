from .create_data import DataCreator
from ..example_models.exceptions import ArgsAndKwargsExcpetion


class ExampleModel(DataCreator):
    @classmethod
    def create(
        cls,
        model,
        quantity: int = 1,
        in_bulk: bool = False,
        full_all_fields: bool = True,
        **kwargs
    ):
        if quantity > 1:
            if in_bulk:
                return cls().get_model_manager(model).bulk_create(*[
                    model(
                        cls().inspect_model(model, **kwargs)
                    ) for number in range(quantity)
                ])
            else:
                return [cls().create_model(model, **kwargs) for number in range(quantity)]
        else:
            if full_all_fields:
                model_data = cls().inspect_model(model, **kwargs)
                kwargs.update(model_data)
            return cls().create_model(model, **kwargs)


    def get_model_manager(self, model: type) -> type:
        try:
            manager = model._default_manager
        except AttributeError:
            manager = model.objects
        finally:
            return manager

    def create_model(self, model: type, **kwargs) -> type:
        return self.get_model_manager(model).create(**kwargs)

    def inspect_model(self, model: type, **kwargs) -> dict:
        fields_info = dict()
        # all_model_fields = model._meta.get_fields()
        for field in model._meta.fields:
            field_name = field.name
            if field_name == "id":
                continue

            if field_name in kwargs:
                fields_info[field_name] = kwargs.pop(field_name)
            else:
                fields_info.update(self.inspect_field(field, field_name, **kwargs))
        return fields_info

    def inspect_field(self, field: type, field_name: str,  **kwargs) -> dict:
        field_type = field.get_internal_type()
        # kwargs.update(field.__dict__)
        return {field_name: self.generate_random_data_per_field(field_type, **kwargs)}

    def generate_random_data_per_field(
        self,
        field_type: str,
        **kwargs
    ):
        data_generator = {
            "DateTimeField": ExampleModel.create_random_datetime,
            "DateField": ExampleModel.create_random_date,
            "TimeField": ExampleModel.create_random_hour,
            # "DurationField": ExampleModel.create(),
            # "AutoField": ExampleModel.create(),
            # "BigAutoField": ExampleModel.create(),
            # "SmallAutoField": ExampleModel.create(),
            # "BinaryField": ExampleModel.create(),
            # "CommaSeparatedIntegerField": ExampleModel.create(),
            "DecimalField": ExampleModel.create_random_float, #(),
            "FloatField": ExampleModel.create_random_float, #(),
            "BigIntegerField": ExampleModel.create_random_integer, #(min_value=10000),
            "PositiveBigIntegerField": ExampleModel.create_random_positive_integer, #(min_value=10000),
            "PositiveIntegerField": ExampleModel.create_random_positive_integer, #(),
            "PositiveSmallIntegerField": ExampleModel.create_random_positive_integer, #(max_value=10000),
            "IntegerField": ExampleModel.create_random_integer, #(),
            "SmallIntegerField": ExampleModel.create_random_integer, #(max_value=10000),

            "CharField": ExampleModel.create_random_string,
            "TextField": ExampleModel.create_random_string,

            "SlugField": ExampleModel.create_random_slug,

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

            "BooleanField": ExampleModel.create_random_bool,
            "NullBooleanField": ExampleModel.create_random_bool,

            "ForeignKey": self.create_model,
            "OneToOneField": self.create_model,
            # "ManyToManyField": ExampleModel.alg(),
        }
        return data_generator[field_type](**kwargs)


