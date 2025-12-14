from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.serializers.login import LoginSerializer
from users.utils import create_token


class LoginView(generics.GenericAPIView):
    """
    Returns authentication token upon successful login.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'fullname': user.profile.full_name,
                    'email': user.email,
                },
                'token': create_token(user),
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)