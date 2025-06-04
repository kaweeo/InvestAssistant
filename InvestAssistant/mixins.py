class PlaceholderMixin:
    def add_placeholders(self):
        for field_name, field in self.fields.items():
            placeholder = field.label or field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholders()


class ReadOnlyMixin:
    read_only_fields = []

    def make_fields_readonly(self):
        fields_to_make_readonly = (
            self.fields.keys() 
            if self.read_only_fields == '__all__' 
            else self.read_only_fields
        )
        
        for field_name in fields_to_make_readonly:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['readonly'] = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_fields_readonly()