import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator:
    def __call__(self, value: str) -> None:
        if not all(c.isalpha() or c.isspace() or c in "-'" for c in value):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes")


@deconstructible
class BasicPhoneNumberValidator:
    def __call__(self, value: str) -> None:
        if not value.isdigit():
            raise ValidationError("Phone number can only contain digits")


@deconstructible
class CustomEmailValidator:
    def __call__(self, value: str) -> None:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_regex, value):
            raise ValidationError(f"'{value}' is not a valid email address.")
