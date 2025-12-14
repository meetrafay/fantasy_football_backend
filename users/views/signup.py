from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.serializers.signup import UserSerializer
from users.utils import create_token


class SignupView(generics.CreateAPIView):
    """
    Creates a user, profile, and assigns to Inventory Managers group.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully.',
                'user': {
                    'id': user.id,
                    'full_name': user.profile.full_name,
                    'email': user.email,
                },
                    
                'token': create_token(user),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)