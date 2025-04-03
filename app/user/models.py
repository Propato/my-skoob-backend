from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, name, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must be assigned to is_staff=True."))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must be assigned to is_superuser=True."))
        
        return self.create_user(name, email, password, **other_fields)
    
    def create_user(self, name, email, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **other_fields)

        user.set_password(password)
        user.save()
        return user
        
class UserProfile(AbstractBaseUser, PermissionsMixin):
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
    # password = models.CharField(max_length=200)

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

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    @property
    def years(self):
        if self.birthday is None:
            return 0
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}, {self.years}'
    
    objects = CustomAccountManager()

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     related_name='skoobuser_groups',
    #     blank=True,
    #     help_text=_('The groups this user belongs to.'),
    #     verbose_name=_('groups'),
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     related_name='skoobuser_permissions',
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     verbose_name=_('user permissions'),
    # )
    