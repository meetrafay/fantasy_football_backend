from rest_framework import serializers

from transactions.models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """
    buyer = serializers.StringRelatedField()
    seller = serializers.StringRelatedField()
    player = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = ["id", "buyer", "seller", "player", "amount", "created_at"]
        read_only_fields = fields
