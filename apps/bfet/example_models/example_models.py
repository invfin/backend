from .create_data import DataCreator


class ExampleModel(DataCreator):
    def __init__(
        self,
        model,
        quantity: int,
        in_bulk: bool,
        full_all_fields: bool,
    ) -> None:
        self.model = model
        self.quantity = quantity
        self.in_bulk = in_bulk
        self.full_all_fields = full_all_fields

    @classmethod
    def create(
        cls,
        model,
        quantity: int = 1,
        in_bulk: bool = False,
        full_all_fields: bool = True,
        **kwargs
    ):
        creator = cls(model, quantity, in_bulk, full_all_fields)
        if quantity > 1:
            if in_bulk:
                return creator.create_in_bulk(**kwargs)
            else:
                return [creator.create_model(**kwargs) for number in range(quantity)]
        else:
            return creator.create_model(**kwargs)

    def get_model_manager(self) -> type:
        try:
            manager = self.model._default_manager
        except AttributeError:
            manager = self.model.objects
        finally:
            return manager

    def create_in_bulk(self, **kwargs):
        pre_objects = [
            self.model(
                **self.inspect_model(**kwargs)
            ) for number in range(self.quantity)
        ]
        return self.get_model_manager().bulk_create(pre_objects)

    def create_model(self, **kwargs) -> type:
        model_data = self.inspect_model(**kwargs)
        kwargs.update(model_data)
        return self.get_model_manager().create(**kwargs)

    def inspect_model(self, **kwargs) -> dict:
        fields_info = dict()
        # all_model_fields = model._meta.get_fields()
        for field in self.model._meta.fields:
            field_name = field.name
            if field_name == "id":
                continue
            if field_name in kwargs:
                fields_info[field_name] = kwargs.pop(field_name)
            else:
                if self.full_all_fields is False:
                    field_allow_null = field.__dict__.get("null")
                    if field_allow_null and field_allow_null is True:
                        fields_info.update({field_name: None})
                        continue

                fields_info.update(self.inspect_field(field, field_name))

        return fields_info

    def inspect_field(self, field: type, field_name: str) -> dict:
        field_type = field.get_internal_type()
        field_specs = field.__dict__
        max_length = field_specs.get("max_length")
        extra_params = {}
        if max_length:
            extra_params["max_value"] = max_length
        return {field_name: self.generate_random_data_per_field(field_type, **extra_params)}

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
            "TextField": ExampleModel.create_random_text,
            "SlugField": ExampleModel.create_random_slug,

            "URLField": ExampleModel.create_random_url,
            "UUIDField": ExampleModel.create_random_uuid,
            "EmailField": ExampleModel.create_random_email,

            # "Empty": ExampleModel.create(),
            # "Field": ExampleModel.create(),
            # "NOT_PROVIDED": ExampleModel.create(),

            # "FilePathField": ExampleModel.create(),
            "FileField": self.return_none_by_now,
            "ImageField": self.return_none_by_now,
            "JSONField": ExampleModel.create_random_json,

            # "GenericIPAddressField": ExampleModel.create(),
            # "IPAddressField": ExampleModel.create(),

            "BooleanField": ExampleModel.create_random_bool,
            "NullBooleanField": ExampleModel.create_random_bool,

            "ForeignKey": self.return_none_by_now,
            "OneToOneField": self.return_none_by_now,
            "ManyToManyField": self.return_none_by_now,
        }
        return data_generator[field_type](**kwargs)

    def return_none_by_now(self, **kwargs):
        return None


