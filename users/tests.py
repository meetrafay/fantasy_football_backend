from django.test import TestCase
from django.contrib.auth.models import User

from users.services.registration import RegistrationService
from users.services.authentication import AuthenticationService
from users.models.user_profile import UserProfile


class UserServicesTestCase(TestCase):
    def test_register_user_creates_user_profile_and_team(self):
        data = {
            "email": "testuser@example.com",
            "password": "strongpassword",
            "username": "Test User",
            "country": "Wonderland",
        }
        user = RegistrationService.register_user(data)
        # user created
        self.assertIsInstance(user, User)
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())
        # profile created
        self.assertTrue(hasattr(user, "profile"))
        self.assertIsInstance(user.profile, UserProfile)
        # team created by TeamCreationService (20 players)
        team = user.profile.team
        self.assertIsNotNone(team)
        self.assertEqual(team.players.count(), 20)

    def test_authentication_service_returns_user_on_valid_credentials(self):
        # create user
        created = User.objects.create_user(
            username="loginuser@example.com", email="loginuser@example.com", password="secret123"
        )
        data = {"email": "loginuser@example.com", "password": "secret123"}
        user = AuthenticationService.login_user(data)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, created.email)
