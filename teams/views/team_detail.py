from rest_framework import permissions, status, generics
from rest_framework.response import Response

from teams.serializer.team import TeamSerializer
from teams.services.team_creation import TeamCreationService


class MyTeamDetailView(generics.GenericAPIView):
    """
    Returns the current user's team + all players.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer

    def get(self, request, *args, **kwargs):
        team = TeamCreationService.get_or_create_team_for_user(request.user.profile)
        serializer = self.get_serializer(team)
        return Response(
            {
                "message": "Team retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        ) 
    