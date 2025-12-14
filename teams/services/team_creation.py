from django.db import transaction

from teams.models.team import Team
from teams.services.player_generation import PlayerGenerationService


class TeamCreationService:
    """
    Service class for creating a Team for a user profile.
    """
    @staticmethod
    @transaction.atomic
    def get_or_create_team_for_user(profile):
        """
        Create a Team for the user and generate players using PlayerGenerationService.
        If a Team exists, return it.
        """
        team, created = Team.objects.get_or_create(
            i_profile=profile,
            name=f"{profile.full_name}'s Team")
        if created:
            # generate default players for that team
            PlayerGenerationService.generate_default_players(team)
        return team
