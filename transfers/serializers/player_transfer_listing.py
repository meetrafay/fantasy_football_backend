from rest_framework import serializers

from transfers.services.transfer_listing import TransferListingService


class ListPlayerSerializer(serializers.Serializer):
    """
    Serializer for listing a player on the transfer market.
    """
    player_id = serializers.IntegerField()
    price = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        player_id = attrs["player_id"]
        price = attrs["price"]
        user = self.context["request"].user

        # Delegate validation rules to the service
        TransferListingService.validate_listing(user, player_id, price)

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        return TransferListingService.create_listing(
            user=user,
            player_id=validated_data["player_id"],
            price=validated_data["price"]
        )
