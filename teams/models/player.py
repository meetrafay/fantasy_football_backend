from django.db import models

from teams.models.team import Team


class Player(models.Model):
    """Model representing a player in a team."""
    POSITION_GK = 'GK'
    POSITION_DF = 'DF'
    POSITION_MF = 'MF'
    POSITION_FW = 'FW'
    POSITION_CHOICES = [
        (POSITION_GK, 'Goalkeeper'),
        (POSITION_DF, 'Defender'),
        (POSITION_MF, 'Midfielder'),
        (POSITION_FW, 'Attacker'),
    ]

    name = models.CharField(max_length=120)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    value = models.BigIntegerField(default=1_000_000)  # initial value $1,000,000
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.position})"