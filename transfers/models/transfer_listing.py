from django.db import models

from teams.models.player import Player
from users.models.user_profile import UserProfile


class TransferListing(models.Model):
    """Model representing a transfer listing for a player."""
    player = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        related_name="listing"
    )
    seller = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    price = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} listed by {self.seller} for {self.price}"
