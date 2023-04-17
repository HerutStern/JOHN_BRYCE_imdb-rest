# https://docs.djangoproject.com/en/4.1/ref/validators/#writing-validators
import datetime

from django.core.exceptions import ValidationError



def validate_year_before_now(val):
    if val > datetime.datetime.today().year:
        raise ValidationError("The year is in the future")



class MinAgeValidator:
    def __init__(self, age):
        self.age = age

    def __call__(self, value):
        if datetime.datetime.now().year - value < self.age:
            raise ValidationError(f"The actor is too young! "
                                  f"We allow only actors older than {self.age} years old")


# my_validator = MinAgeValidator(5)
# my_validator(1998)
