from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import models

from transactions.models.transaction import Transaction
from transactions.serializers.trasaction import TransactionSerializer


class MyTransactionListView(generics.GenericAPIView):
    """
    Returns transactions where the user is buyer OR seller.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        user = request.user.profile
        transactions = Transaction.objects.filter(
            models.Q(buyer=user) | models.Q(seller=user)
        ).select_related("buyer", "seller", "player").order_by("-created_at")

        serializer = self.get_serializer(transactions, many=True)
        return Response(
            {
                'message': "User transactions retrieved.",
                'data': serializer.data,
            },
            status=status.HTTP_200_OK
        )
