from django.db import transaction
from django.shortcuts import get_object_or_404
from transactions.services.transaction import TransactionService
from transfers.models.transfer_listing import TransferListing
import random

from rest_framework import serializers


class TransferPurchaseService:
    """
    Service class for handling player purchases from the transfer market.
    """
    @staticmethod
    def validate_purchase(buyer, listing_id):
        listing = get_object_or_404(TransferListing, id=listing_id)

        if not listing.is_active:
            raise serializers.ValidationError("This listing is no longer active.")

        if listing.seller == buyer:
            raise serializers.ValidationError("You cannot buy your own player.")

        # ensure buyer has a team
        if not hasattr(buyer, "team"):
            raise serializers.ValidationError("Buyer does not have a team.")

        if buyer.team.capital < listing.price:
            raise serializers.ValidationError("You do not have enough capital to buy this player.")

    @staticmethod
    @transaction.atomic
    def buy_player(buyer, listing_id):
        """
        Process the purchase of a player from the transfer market.
        """
        listing = get_object_or_404(TransferListing, id=listing_id)
        seller = listing.seller
        player = listing.player
        price = listing.price

        buyer_team = buyer.team
        seller_team = seller.team

        # --- Move money ---
        buyer_team.capital -= price
        seller_team.capital += price

        buyer_team.save()
        seller_team.save()

        # --- Transfer ownership ---
        player.team = buyer_team
        player.save()

        # --- Deactivate listing ---
        listing.is_active = False
        listing.save()

        # --- Random value increase ---
        player.value = TransferPurchaseService.increase_player_value(player.value)
        player.save()

        # --- Create transaction record ---
        TransactionService.create_transaction(
            buyer=buyer,
            seller=seller,
            player=player,
            amount=price
        )


        # --- Return final info ---
        return {
            "player_id": player.id,
            "player_name": player.name,
            "new_value": player.value,
            "buyer_team_capital": buyer_team.capital,
            "seller_team_capital": seller_team.capital,
        }

    @staticmethod
    def increase_player_value(current_value):
        """
        Increase value by 1%–10% randomly.
        """
        percentage = random.uniform(0.01, 0.10)
        return int(current_value + current_value * percentage)
