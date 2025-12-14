from rest_framework import generics, permissions, status
from rest_framework.response import Response

from transfers.serializers.player_transfer_listing import ListPlayerSerializer


class ListPlayerForSaleView(generics.GenericAPIView):
    """
    List a player for sale.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListPlayerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        listing = serializer.save()

        return Response(

            {
                'message': "Player listed successfully.",
                'data': {
                    'id': listing.id,
                    'player': listing.player.name,
                    'price': listing.price,
                    'is_active': listing.is_active,
                },
            },
         
            status=status.HTTP_201_CREATED
        )
