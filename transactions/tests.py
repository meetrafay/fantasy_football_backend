from django.test import TestCase
from django.contrib.auth.models import User

from transactions.services.transaction import TransactionService
from users.models.user_profile import UserProfile
from teams.services.team_creation import TeamCreationService


class TransactionServiceTestCase(TestCase):
    def test_create_transaction_records_entry(self):
        # prepare buyer and seller users and profiles
        buyer_user = User.objects.create_user(username="b@example.com", email="b@example.com", password="pwd12345")
        seller_user = User.objects.create_user(username="s@example.com", email="s@example.com", password="pwd12345")
        buyer_profile = UserProfile.objects.create(user=buyer_user, full_name="Buyer", country="X")
        seller_profile = UserProfile.objects.create(user=seller_user, full_name="Seller", country="Y")
        # ensure teams exist
        TeamCreationService.get_or_create_team_for_user(buyer_profile)
        TeamCreationService.get_or_create_team_for_user(seller_profile)
        # create a dummy player owned by seller
        player = seller_profile.team.players.first()
        tx = TransactionService.create_transaction(buyer=buyer_profile, seller=seller_profile, player=player, amount=123456)
        self.assertIsNotNone(tx.id)
        self.assertEqual(tx.amount, 123456)
        self.assertEqual(tx.buyer.id, buyer_profile.id)
        self.assertEqual(tx.seller.id, seller_profile.id)
