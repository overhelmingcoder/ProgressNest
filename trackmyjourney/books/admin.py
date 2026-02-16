from django.contrib import admin
from .models import Book, BookCategory, ReadingList, BookRating

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class BookRatingInline(admin.TabularInline):
    model = BookRating
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded_by', 'format', 'language', 'is_public', 'downloads', 'views')
    list_filter = ('format', 'language', 'is_public', 'is_featured', 'uploaded_at')
    search_fields = ('title', 'author', 'isbn', 'uploaded_by__username')
    date_hierarchy = 'uploaded_at'
    inlines = [BookRatingInline]
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'description')
        }),
        ('File Information', {
            'fields': ('file', 'cover_image', 'format', 'language', 'pages')
        }),
        ('Publication Details', {
            'fields': ('publisher', 'publication_date', 'categories')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'tags', 'is_public', 'is_featured', 'allow_download')
        }),
        ('Statistics', {
            'fields': ('downloads', 'views'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'progress', 'added_at')
    list_filter = ('status', 'added_at')
    search_fields = ('user__username', 'book__title')

@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'book__title')
