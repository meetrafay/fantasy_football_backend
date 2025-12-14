from django.urls import path

from teams.views.team_detail import MyTeamDetailView


urlpatterns = [
    path("my/team/", MyTeamDetailView.as_view(), name="my-team"),
]
