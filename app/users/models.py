from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=200)

    GENDERS = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Others"),
    ]
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True)
    
    def validate_birthday(value):
        today = date.today()
        min_age_date = date(today.year - 12, today.month, today.day)
        if value > min_age_date:
            raise ValidationError(
                _('You must be at least 12 years old.'),
                params={'value': value},
            )
    birthday = models.DateField(blank=True, validators=[validate_birthday])

    @property
    def years(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email', violation_error_message="This email has already been registered")
        ]

    def __str__(self):
        return f'{self.name}, {self.years}'