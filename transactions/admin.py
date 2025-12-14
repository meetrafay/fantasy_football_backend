from django.contrib import admin
from transactions.models.transaction import Transaction

admin.site.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_type', 'created_at')
    search_fields = ('user__username', 'transaction_type')
    list_filter = ('transaction_type',)
    readonly_fields = ('created_at',)