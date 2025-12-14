from django.contrib import admin
from users.models.user_profile import UserProfile


admin.site.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'country', 'created_at')
    search_fields = ('user__username', 'full_name', 'country')
