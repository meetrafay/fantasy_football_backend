from django.urls import path

from transfers.views.buy_player import BuyPlayerView
from transfers.views.player_list import ListPlayerForSaleView
from transfers.views.players_market import MarketListingView


urlpatterns = [
    path("list/player/", ListPlayerForSaleView.as_view(), name="list-player-for-sale"),
    path("players/market/", MarketListingView.as_view(), name="market-listings"),
    path("buy/player/", BuyPlayerView.as_view(), name="buy-player"),
]
