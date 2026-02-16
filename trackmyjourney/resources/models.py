from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import os

User = get_user_model()

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]
    RESOURCE_TYPE_CHOICES = [
        ('article', 'Article'),
        ('tutorial', 'Tutorial'),
        ('template', 'Template'),
        ('guide', 'Guide'),
        ('tool', 'Tool'),
        ('presentation', 'Presentation'),
        ('research', 'Research Paper'),
        ('webinar', 'Webinar'),
        ('podcast', 'Podcast'),
        ('ebook', 'E-book'),
        ('infographic', 'Infographic'),
        ('checklist', 'Checklist'),
        ('worksheet', 'Worksheet'),
        ('case_study', 'Case Study'),
        ('report', 'Report'),
        ('course', 'Course'),
        ('software', 'Software'),
        ('dataset', 'Dataset'),
        ('code', 'Code Snippet'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='document')
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES, default='article')
    file = models.FileField(upload_to='resources/files/', blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL if no file is uploaded (e.g., YouTube link)")
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags (e.g., 'productivity, learning, tech')")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True) # Added field
    is_featured = models.BooleanField(default=False) # Added field

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('resources:detail', kwargs={'pk': self.pk})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1][1:].upper()
        return ''

class ResourceComment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.resource.title}"

class ResourceRating(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)]) # 1 to 5 stars
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.resource.title} {self.rating} stars"

class ResourceLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} likes {self.resource.title}"

class ResourceBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"
