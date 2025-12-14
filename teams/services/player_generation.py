import random

from teams.models.player import Player


class PlayerGenerationService:
    """Service for generating players for a team."""
    @staticmethod
    def generate_default_players(team):
        """
        Create 20 players for the team with distribution:
         - 2 GK
         - 6 DF
         - 6 MF
         - 6 FW
        Player names are auto-generated placeholders; replace with your data source if needed.
        """
        positions = (
            ([Player.POSITION_GK] * 2) +
            ([Player.POSITION_DF] * 6) +
            ([Player.POSITION_MF] * 6) +
            ([Player.POSITION_FW] * 6)
        )

        created_players = []
        for idx, pos in enumerate(positions, start=1):
            # name generation: TeamName_Player_<idx> or random
            name = f"Player {idx} - {team.i_profile.full_name}"
            player = Player.objects.create(
                name=name,
                position=pos,
                value=1_000_000,
                team=team
            )
            created_players.append(player)

        # Optionally shuffle players
        random.shuffle(created_players)
        return created_players
