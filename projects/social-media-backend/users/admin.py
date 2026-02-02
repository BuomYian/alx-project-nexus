"""
Admin configuration for users app.
"""
from django.contrib import admin
from users.models import Profile, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'followers_count', 'following_count', 'created_at')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('created_at', 'updated_at', 'followers_count', 'following_count')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile Info', {'fields': ('bio', 'avatar', 'cover_image')}),
        ('Statistics', {'fields': ('followers_count', 'following_count')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')
    readonly_fields = ('created_at',)
    list_filter = ('created_at',)
