from rest_framework import generics, permissions, status
from rest_framework.response import Response

from transfers.models.transfer_listing import TransferListing
from transfers.serializers.players_market import TransferListingSerializer


class MarketListingView(generics.GenericAPIView):
    """
    Returns all active player listings.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransferListingSerializer

    def get(self, request, *args, **kwargs):
        listings = TransferListing.objects.filter(is_active=True) \
            .select_related("player", "seller") \
            .order_by("-created_at")

        serializer = self.get_serializer(listings, many=True)

        return Response(
            {
                'message': "Active transfer listings retrieved.",
                'data': serializer.data,
            },
            status=status.HTTP_200_OK
        )
