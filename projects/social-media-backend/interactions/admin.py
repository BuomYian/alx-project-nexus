"""
Admin configuration for interactions app.
"""
from django.contrib import admin
from interactions.models import PostLike, CommentLike, Share, View, Notification


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    search_fields = ('user__username', 'comment__content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'shared_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('shared_at',)
    readonly_fields = ('shared_at',)


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'viewed_at')
    search_fields = ('user__username', 'post__title')
    list_filter = ('viewed_at',)
    readonly_fields = ('viewed_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'actor', 'notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'actor__username')
    list_filter = ('notification_type', 'is_read', 'created_at')
    readonly_fields = ('created_at',)
