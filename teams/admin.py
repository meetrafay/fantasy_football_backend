from django.contrib import admin
from teams.models.team import Team
from teams.models.player import Player


admin.site.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)


admin.site.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'team', 'market_value', 'is_for_sale')
    search_fields = ('name', 'team__name')
    list_filter = ('position', 'is_for_sale')




