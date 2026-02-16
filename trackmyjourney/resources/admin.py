from django.contrib import admin
from .models import Resource, ResourceComment, ResourceRating

class ResourceCommentInline(admin.TabularInline):
    model = ResourceComment
    extra = 0

class ResourceRatingInline(admin.TabularInline):
    model = ResourceRating
    extra = 0

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'category', 'resource_type', 'is_public', 'downloads', 'views', 'uploaded_at')
    list_filter = ('category', 'resource_type', 'is_public', 'is_featured', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username', 'description')
    date_hierarchy = 'uploaded_at'
    inlines = [ResourceCommentInline, ResourceRatingInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'uploaded_by')
        }),
        ('Resource Details', {
            'fields': ('category', 'resource_type', 'file', 'url', 'thumbnail')
        }),
        ('Metadata', {
            'fields': ('tags', 'is_public', 'is_featured', 'is_active')
        }),
        ('Statistics', {
            'fields': ('downloads', 'views'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ResourceComment)
class ResourceCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'resource__title', 'content')

@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'resource__title')
