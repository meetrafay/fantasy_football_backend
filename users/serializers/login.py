from rest_framework import serializers

from users.services.authentication import AuthenticationService


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Validate user credentials.
        """
        user = AuthenticationService.login_user(data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user