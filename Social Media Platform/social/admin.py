from django.contrib import admin
from .models import Profile, Post, Comment, Like, Follow, Notification

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'created_at']
    search_fields = ['user__username', 'display_name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at']
    search_fields = ['author__username', 'caption']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'notification_type', 'created_at']
