from rest_framework import serializers
from django.contrib.auth.models import User

from users.services.registration import RegistrationService


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, including profile.
    """
    country = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'country', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'email': {'required': True, 'allow_blank': False},
            'username': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        """
        Validate that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        """
        Create a user with a profile and assign to 'Inventory Managers' group.
        """
        user = RegistrationService.register_user(validated_data)
        return user