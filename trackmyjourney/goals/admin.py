from django.contrib import admin
from .models import Goal, Category, Milestone, GoalUpdate

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Corrected: Only 'name' exists in your Category model based on models.py
    list_display = ['name']
    search_fields = ['name']

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0

class GoalUpdateInline(admin.TabularInline):
    model = GoalUpdate
    extra = 0
    readonly_fields = ['created_at']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'progress', 'target_date', 'created_at']
    list_filter = ['status', 'priority', 'category', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    inlines = [MilestoneInline, GoalUpdateInline]

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'target_date', 'created_at']
    search_fields = ['title', 'goal__title']

@admin.register(GoalUpdate)
class GoalUpdateAdmin(admin.ModelAdmin):
    list_display = ['goal', 'user', 'progress_change', 'created_at']
    list_filter = ['created_at']
    search_fields = ['goal__title', 'user__username', 'content']
    readonly_fields = ['created_at']
