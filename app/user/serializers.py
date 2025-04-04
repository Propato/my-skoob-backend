from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        # extra_kwargs = { "password": { "write_only": True }}

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        many_to_many_fields = ['groups', 'user_permissions']
        for field in many_to_many_fields:
            if field in validated_data:
                getattr(instance, field).set(validated_data[field])
                validated_data.pop(field, None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
    def validate_password(self, password):
        try:
            validate_password(password)
            return password
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})