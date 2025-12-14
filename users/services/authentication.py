from django.contrib.auth import authenticate

class AuthenticationService:
    """
    Service class for handling user authentication.
    """
    @staticmethod
    def login_user(validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        user = authenticate(username=email, password=password)
        return user
