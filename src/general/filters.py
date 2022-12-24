from django.contrib.admin import SimpleListFilter


class JSONFieldFilter(SimpleListFilter):
    json_field_name: str = ""
    json_field_property_name: str = ""

    def __init__(self, request, params, model, model_admin):
        super(JSONFieldFilter, self).__init__(request, params, model, model_admin)

        assert hasattr(self, "title"), 'Class {} missing "title" attribute'.format(self.__class__.__name__)
        assert hasattr(self, "parameter_name"), 'Class {} missing "parameter_name" attribute'.format(
            self.__class__.__name__
        )
        assert hasattr(self, "json_field_name"), 'Class {} missing "json_field_name" attribute'.format(
            self.__class__.__name__
        )
        assert hasattr(
            self, "json_field_property_name"
        ), 'Class {} missing "json_field_property_name" attribute'.format(self.__class__.__name__)

    def lookups(self, request, model_admin):
        """
        # Improvemnt needed: if the size of jsonfield is large and there are lakhs of row
        """
        if "__" in self.json_field_property_name:  # NOTE: this will cover only one nested level
            keys = self.json_field_property_name.split("__")
            field_value_set = set(
                data[keys[0]][keys[1]]
                for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
        else:
            field_value_set = set(
                data[self.json_field_property_name]
                for data in model_admin.model.objects.values_list(self.json_field_name, flat=True)
            )
            return [(v, v) for v in field_value_set]

    def queryset(self, request, queryset):
        if self.value():
            json_field_query = {"{}__{}".format(self.json_field_name, self.json_field_property_name): self.value()}
            return queryset.filter(**json_field_query)
        else:
            return queryset


# Now Extend this class to create custom admin filter for JSON field properties.
