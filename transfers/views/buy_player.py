from rest_framework import generics, permissions, status
from rest_framework.response import Response

from transfers.serializers.buy_player import BuyPlayerSerializer


class BuyPlayerView(generics.GenericAPIView):
    """
    Buy a listed player.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BuyPlayerSerializer

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

        result = serializer.save()

        return Response(
            {
                'message': "Player purchased successfully.",
                'data': result,
            },
            status=status.HTTP_200_OK
        )
