from django.db import models
from django.contrib.auth.models import User
from users.models.user_profile import UserProfile
from teams.models.player import Player

class Transaction(models.Model):
    """Model representing a transaction of a player between users."""
    buyer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="purchases"
    )
    seller = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sales"
    )
    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player} bought by {self.buyer} from {self.seller} for {self.amount}"
