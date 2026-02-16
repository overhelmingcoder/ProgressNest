from django.contrib import admin
from .models import Achievement, AchievementComment

class AchievementCommentInline(admin.TabularInline):
    model = AchievementComment
    extra = 0

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'badge_type', 'date_achieved', 'is_public', 'total_likes')
    list_filter = ('category', 'badge_type', 'is_public', 'date_achieved')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'date_achieved'
    inlines = [AchievementCommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Achievement Details', {
            'fields': ('category', 'badge_type', 'image', 'date_achieved')
        }),
        ('Settings', {
            'fields': ('is_public',)
        }),
    )

@admin.register(AchievementComment)
class AchievementCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'achievement__title', 'content')
