from django.contrib import admin
from .models import BlogPost, Category, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'is_featured', 'views', 'total_likes', 'created_at')
    list_filter = ('status', 'is_featured', 'created_at', 'categories')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [CommentInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Classification', {
            'fields': ('categories', 'tags')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'allow_comments')
        }),
        ('Stats', {
            'fields': ('views', 'reading_time'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author__username', 'post__title', 'content')
