from rest_framework import serializers

from transfers.services.player_purchase import TransferPurchaseService


class BuyPlayerSerializer(serializers.Serializer):
    """
    Serializer for purchasing a player from the transfer market.
    """
    listing_id = serializers.IntegerField()

    def validate(self, attrs):
        listing_id = attrs["listing_id"]
        user = self.context["request"].user.profile

        # Delegate validation rules to the service
        TransferPurchaseService.validate_purchase(user, listing_id)

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user.profile
        listing_id = validated_data["listing_id"]
        return TransferPurchaseService.buy_player(user, listing_id)
