from django.db import models

from users.models.user_profile import UserProfile



class Team(models.Model):
    """Model representing a team associated with a user profile."""
    i_profile = models.OneToOneField(
        UserProfile, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="team"
    )
    name = models.CharField(max_length=150)
    capital = models.BigIntegerField(default=5_000_000)  # store cents/units as integers
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.i_profile.user.username}'s Team"

    @property
    def total_value(self):
        # Sum of player values
        return self.players.aggregate(total=models.Sum('value'))['total'] or 0