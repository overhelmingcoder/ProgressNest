from django.contrib import admin
from .models import Community, Post, CommunityMembership, PostLike, Comment

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'member_count', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['moderators']
    readonly_fields = ['created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'community', 'like_count', 'created_at']
    list_filter = ['community', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CommunityMembership)
class CommunityMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'community', 'is_moderator', 'joined_at']
    list_filter = ['is_moderator', 'joined_at']
    search_fields = ['user__username', 'community__name']

admin.site.register(PostLike)
admin.site.register(Comment)
