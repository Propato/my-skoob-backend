from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

    # def validate_email(self, value):
    #     if self.instance and self.instance.email == value:
    #         return value

    #     if Users.objects.filter(email=value).exists():
    #         raise ValidationError(
    #             _("This email has already been registered"),
    #             params={'value': value},
    #         )
    #     return value

    # def validate(self, attrs):
    #     attrs['email'] = self.validate_email(attrs.get('email'))
    #     return super().validate(attrs)
