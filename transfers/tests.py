from django.test import TestCase
from django.contrib.auth.models import User

from users.services.registration import RegistrationService
from transfers.services.transfer_listing import TransferListingService
from transfers.services.player_purchase import TransferPurchaseService
from transfers.models.transfer_listing import TransferListing
from transactions.models.transaction import Transaction


class TransfersIntegrationTestCase(TestCase):
    def setUp(self):
        # create seller and buyer via registration (teams + players created)
        seller_data = {
            "email": "seller@example.com",
            "password": "sellerpass",
            "username": "Seller",
            "country": "S"
        }
        buyer_data = {
            "email": "buyer@example.com",
            "password": "buyerpass",
            "username": "Buyer",
            "country": "B"
        }
        self.seller_user = RegistrationService.register_user(seller_data)
        self.buyer_user = RegistrationService.register_user(buyer_data)
        # pick a player owned by seller
        self.seller_team = self.seller_user.profile.team
        self.buyer_team = self.buyer_user.profile.team
        self.player = self.seller_team.players.first()

    def test_list_and_buy_player_flow(self):
        # create listing by seller
        listing = TransferListingService.create_listing(self.seller_user, self.player.id, price=2_000_000)
        self.assertIsInstance(listing, TransferListing)
        self.assertTrue(listing.is_active)
        # validate buyer can purchase
        TransferPurchaseService.validate_purchase(self.buyer_user.profile, listing.id)
        result = TransferPurchaseService.buy_player(self.buyer_user.profile, listing.id)
        # assert ownership transferred
        self.player.refresh_from_db()
        self.assertEqual(self.player.team.id, self.buyer_team.id)
        # listing deactivated
        listing.refresh_from_db()
        self.assertFalse(listing.is_active)
        # capitals updated
        self.buyer_team.refresh_from_db()
        self.seller_team.refresh_from_db()
        self.assertLess(self.buyer_team.capital, 5_000_000)
        self.assertGreater(self.seller_team.capital, 5_000_000)
        # transaction created
        self.assertTrue(Transaction.objects.filter(player=self.player).exists())
        tx = Transaction.objects.filter(player=self.player).first()
        self.assertEqual(tx.amount, listing.price)
