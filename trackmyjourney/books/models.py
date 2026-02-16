from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
import os

User = get_user_model()

class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')

    class Meta:
        verbose_name_plural = 'Book Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:category_detail', kwargs={'slug': self.slug})

class Book(models.Model):
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('mobi', 'MOBI'),
        ('txt', 'Text'),
        ('doc', 'Word Document'),
        ('other', 'Other'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('ar', 'Arabic'),
        ('hi', 'Hindi'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, blank=True, null=True, unique=True)
    description = models.TextField()
    categories = models.ManyToManyField(BookCategory, related_name='books')
    
    # File information
    file = models.FileField(upload_to='books/files/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    pages = models.PositiveIntegerField(blank=True, null=True)
    
    # Metadata
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_books')
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    # Settings
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    allow_download = models.BooleanField(default=True)
    
    # Stats
    downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_books', blank=True)
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.author}")
            original_slug = self.slug
            counter = 1
            while Book.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def file_size(self):
        if self.file:
            return self.file.size
        return 0

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_bookmarks(self):
        return self.bookmarks.count()

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return sum(r.rating for r in ratings) / len(ratings)
        self.downloads += 1
        self.save(update_fields=['downloads'])

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class ReadingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status_choices = [
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('read', 'Read'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='want_to_read')
    progress = models.PositiveIntegerField(default=0, help_text="Reading progress percentage")
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"

class BookRating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['book', 'user']

    def __str__(self):
        return f"{self.user.username} rated {self.book.title}: {self.rating}/5"
