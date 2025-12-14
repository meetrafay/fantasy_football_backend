from rest_framework import serializers

from teams.models.player import Player


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model.
    """
    class Meta:
        model = Player
        fields = ["id", "name", "position", "value", "created_at"]
        read_only_fields = ["id", "value", "created_at"]