from django.shortcuts import get_object_or_404
from django.db import transaction
from teams.models.player import Player
from transfers.models.transfer_listing import TransferListing
from rest_framework import serializers

class TransferListingService:
    """
    Service class for handling transfer listings.
    """
    @staticmethod
    def validate_listing(user, player_id, price):
        player = get_object_or_404(Player, id=player_id)

        # 1. Must be owner
        if player.team.i_profile.user != user:
            raise serializers.ValidationError("You can only list players you own.")

        # 2. Cannot list twice
        if hasattr(player, "listing") and player.listing.is_active:
            raise serializers.ValidationError("This player is already listed.")

        # 3. Price must be higher than player's current value
        if price <= player.value:
            raise serializers.ValidationError(
                f"Listing price must be greater than player's value ({player.value})."
            )

    @staticmethod
    @transaction.atomic
    def create_listing(user, player_id, price):
        player = get_object_or_404(Player, id=player_id)

        listing = TransferListing.objects.create(
            player=player,
            seller=user.profile,
            price=price,
            is_active=True
        )
        return listing
