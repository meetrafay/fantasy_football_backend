from rest_framework import serializers

from teams.models.team import Team
from teams.serializer.player import PlayerSerializer


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model, including related players.
    """
    i_profile = serializers.StringRelatedField(read_only=True)
    capital = serializers.IntegerField(read_only=True)
    total_value = serializers.SerializerMethodField()
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "i_profile", "name", "capital", "total_value", "players", "created_at"]
        read_only_fields = ["id", "i_profile", "name", "capital", "total_value", "players", "created_at"]

    def get_total_value(self, obj):
        # We return aggregated team value
        return obj.total_value
