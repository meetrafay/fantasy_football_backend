from django.urls import path

from transactions.views.all_transactions import TransactionListView
from transactions.views.my_transactions import MyTransactionListView


urlpatterns = [
    path("all/transactions/", TransactionListView.as_view(), name="all-transactions"),
    path("my/transactions/", MyTransactionListView.as_view(), name="my-transactions"),

]
