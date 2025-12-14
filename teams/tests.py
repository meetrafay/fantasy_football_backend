from django.test import TestCase
from django.contrib.auth.models import User

from teams.services.team_creation import TeamCreationService
from users.models.user_profile import UserProfile


class TeamCreationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teamuser@example.com", email="teamuser@example.com", password="pwd123456"
        )
        self.profile = UserProfile.objects.create(user=self.user, full_name="Team User", country="UT")

    def test_get_or_create_team_for_user_creates_team_once(self):
        team = TeamCreationService.get_or_create_team_for_user(self.profile)
        self.assertIsNotNone(team)
        # second call should return same team, not create new
        team2 = TeamCreationService.get_or_create_team_for_user(self.profile)
        self.assertEqual(team.id, team2.id)
        # confirm players generated (20)
        self.assertEqual(team.players.count(), 20)
