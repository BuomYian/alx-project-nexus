"""
Admin configuration for posts app.
"""
from django.contrib import admin
from posts.models import Post, Comment, Hashtag, Mention


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('created_at', 'is_published')
    readonly_fields = ('created_at', 'updated_at', 'search_vector')
    fieldsets = (
        ('Content', {'fields': ('author', 'title', 'content', 'image')}),
        ('Tags', {'fields': ('hashtags',)}),
        ('Status', {'fields': ('is_published',)}),
        ('Search', {'fields': ('search_vector',), 'classes': ('collapse',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'is_edited')
    search_fields = ('content', 'author__username', 'post__title')
    list_filter = ('created_at', 'is_edited')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Content', {'fields': ('post', 'author', 'content', 'parent')}),
        ('Status', {'fields': ('is_edited',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'post_count', 'created_at')
    search_fields = ('tag',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Tag', {'fields': ('tag',)}),
        ('Info', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ('mentioned_user', 'post', 'created_at')
    search_fields = ('mentioned_user__username', 'post__title')
    list_filter = ('created_at', 'mentioned_user')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Mention', {'fields': ('post', 'mentioned_user')}),
        ('Info', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
