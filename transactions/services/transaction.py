from transactions.models.transaction import Transaction


class TransactionService:
    """
    Service class for handling transactions.
    """
    @staticmethod
    def create_transaction(buyer, seller, player, amount):
        return Transaction.objects.create(
            buyer=buyer,
            seller=seller,
            player=player,
            amount=amount
        )
