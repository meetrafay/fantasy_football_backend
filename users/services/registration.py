from django.contrib.auth.models import User
from django.db import transaction

from teams.services.team_creation import TeamCreationService
from users.models.user_profile import UserProfile


class RegistrationService:
    """
    Service class for handling user registration.
    """
    @staticmethod
    @transaction.atomic
    def register_user(validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        profile = UserProfile.objects.create(
            user=user,
            full_name=validated_data['username'],
            country=validated_data['country']
        )
        
        # Trigger handler to create team & players
        TeamCreationService.get_or_create_team_for_user(profile)
        return user
