from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Watchlist, UserProfile

admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'description')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
