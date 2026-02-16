from django.contrib import admin
from .models import ContactMessage, HomePageSettings, FakePost

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    actions = [mark_as_read]

@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Content', {
            'fields': ('about_text', 'goal_text')
        }),
        ('Statistics', {
            'fields': ('users_count', 'collaborations_count')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
    )

@admin.register(FakePost)
class FakePostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'created_at', 'likes_count', 'comments_count']
    list_filter = ['created_at']
    search_fields = ['title', 'content', 'author_name']
    readonly_fields = ['created_at']
