from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

class Users(models.Model):
    def validate_birthday(value):
        today = date.today()
        min_age_date = date(today.year - 12, today.month, today.day)
        if value > min_age_date:
            raise ValidationError(
                _('You must be at least 12 years old.'),
                params={'value': value},
            )
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60, unique=True)
    password = models.CharField(max_length=200)

    GENDERS = [
        ("FC", "Female Cis"),
        ("MC", "Male Cis"),
        ("FT", "Female Trans"),
        ("MT", "Male Trans"),
        ("N", "Non-Binary"),
        ("O", "Others"),
    ]
    gender = models.CharField(max_length=2, choices=GENDERS, null=True)
    
    birthday = models.DateField(null=True, validators=[validate_birthday])

    @property
    def years(self):
        if self.birthday is None:
            return 0
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    def __str__(self):
        return f'{self.name}, {self.years}'