from django.contrib import admin
from transfers.models.transfer_listing import TransferListing

admin.site.register(TransferListing)
class TransferListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'selling_team', 'buying_team', 'price', 'status', 'created_at')
    search_fields = ('player__name', 'selling_team__user__username', 'buying_team__user__username')
    list_filter = ('status',)

