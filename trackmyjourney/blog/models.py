from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('cybersecurity', 'Cybersecurity'),
        ('machine-learning', 'Machine Learning'),
        ('artificial-intelligence', 'Artificial Intelligence'),
        ('data-science', 'Data Science'),
        ('web-development', 'Web Development'),
        ('mobile-development', 'Mobile Development'),
        ('cloud-computing', 'Cloud Computing'),
        ('blockchain', 'Blockchain'),
        ('health-tech', 'Health & Technology'),
        ('fintech', 'Financial Technology'),
        ('research', 'Research & Academia'),
        ('tech-news', 'Technology News'),
        ('programming', 'Programming'),
        ('software-engineering', 'Software Engineering'),
        ('devops', 'DevOps'),
        ('ui-ux', 'UI/UX Design'),
        ('career', 'Career & Professional'),
        ('tutorials', 'Tutorials & How-to'),
        ('reviews', 'Product Reviews'),
        ('opinion', 'Opinion & Analysis'),
        ('startup', 'Startup & Entrepreneurship'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Hex color code")
    icon = models.CharField(max_length=50, default='fas fa-folder', help_text="FontAwesome icon class")
    is_featured = models.BooleanField(default=False)
    post_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def update_post_count(self):
        self.post_count = self.posts.filter(status='published').count()
        self.save(update_fields=['post_count'])

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.TextField()
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_posts', blank=True)
    reading_time = models.PositiveIntegerField(default=1, help_text="Estimated reading time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure unique slug
            original_slug = self.slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        if not self.excerpt and self.content:
            # Create excerpt from content
            words = self.content.split()[:50]
            self.excerpt = ' '.join(words) + ('...' if len(words) == 50 else '')
        
        # Calculate reading time
        if self.content:
            word_count = len(self.content.split())
            self.reading_time = max(1, word_count // 200)  # 200 words per minute
        
        # Set published_at when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
        
        # Update category post counts
        for category in self.categories.all():
            category.update_post_count()

    @property
    def total_likes(self):
        return self.likes.count()
    
    @property
    def total_bookmarks(self):
        return self.bookmarks.count()
    
    @property
    def total_comments(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    @property
    def total_likes(self):
        return self.likes.count()
