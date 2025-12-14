from rest_framework import generics, permissions, status
from rest_framework.response import Response
from transactions.models.transaction import Transaction
from transactions.serializers.trasaction import TransactionSerializer


class TransactionListView(generics.GenericAPIView):
    """
    Returns ALL transactions in the system.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.select_related(
            "buyer", "seller", "player"
        ).order_by("-created_at")

        serializer = self.get_serializer(transactions, many=True)
        return Response(
            {
                'message': "All transactions retrieved.",
                'data': serializer.data,

            },
            status=status.HTTP_200_OK
        )
