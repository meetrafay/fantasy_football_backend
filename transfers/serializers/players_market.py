from rest_framework import serializers

from transfers.models.transfer_listing import TransferListing


class TransferListingSerializer(serializers.ModelSerializer):
    """
    Serializer for the TransferListing model.
    """
    player_name = serializers.CharField(source="player.name", read_only=True)
    player_position = serializers.CharField(source="player.position", read_only=True)
    current_value = serializers.IntegerField(source="player.value", read_only=True)
    # seller = serializers.StringRelatedField(read_only=True)
    seller = serializers.CharField(source="seller.profile.full_name", read_only=True)
    team = serializers.CharField(source="seller.team.name", read_only=True)

    class Meta:
        model = TransferListing
        fields = [
            "id",
            "team",
            "player_name",
            "player_position",
            "current_value",
            "price",
            "seller",
            "is_active",
            "created_at",
        ]
        read_only_fields = fields
