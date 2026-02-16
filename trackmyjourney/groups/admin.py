from django.contrib import admin
from .models import Group, GroupMembership, GroupPost, GroupPostComment

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'category', 'privacy', 'member_count', 'is_featured', 'created_at')
    list_filter = ('category', 'privacy', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'creator__username', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GroupMembershipInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'creator')
        }),
        ('Group Details', {
            'fields': ('category', 'privacy', 'cover_image', 'logo', 'rules')
        }),
        ('Settings', {
            'fields': ('allow_member_posts', 'require_approval', 'is_featured', 'is_active')
        }),
        ('Metadata', {
            'fields': ('tags', 'member_count', 'post_count'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'status', 'joined_at')
    list_filter = ('role', 'status', 'joined_at')
    search_fields = ('user__username', 'group__name')

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'group', 'is_pinned', 'is_approved', 'total_likes', 'created_at')
    list_filter = ('is_pinned', 'is_approved', 'created_at')
    search_fields = ('title', 'author__username', 'group__name')

@admin.register(GroupPostComment)
class GroupPostCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'post__title', 'content')
