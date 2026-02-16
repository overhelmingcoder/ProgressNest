from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

class Community(models.Model):
    CATEGORY_CHOICES = [
        ('health', 'Health & Fitness'),
        ('tech', 'Technology'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('business', 'Business'),
        ('lifestyle', 'Lifestyle'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    banner = models.ImageField(upload_to='community_banners/', blank=True, null=True)
    logo = models.ImageField(upload_to='community_logos/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    rules = models.TextField(help_text="Enter rules separated by newlines", blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_created_communities')
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='community_moderated_communities', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CommunityMembership', related_name='community_joined_communities')

    class Meta:
        verbose_name_plural = "Communities"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('community:detail', kwargs={'pk': self.pk})
    
    @property
    def member_count(self):
        return self.members.count()
    
    @property
    def posts_per_day(self):
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_posts = self.posts.filter(created_at__gte=thirty_days_ago).count()
        return round(recent_posts / 30, 1)
    
    @property
    def rules_list(self):
        if self.rules:
            return [rule.strip() for rule in self.rules.split('\n') if rule.strip()]
        return []

class CommunityMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_memberships')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_memberships')
    joined_at = models.DateTimeField(default=timezone.now)
    is_moderator = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'community')

class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_posts')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PostLike', related_name='community_liked_posts')
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='community_bookmarked_posts', blank=True)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.pk})
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()
    
    @property
    def tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_post_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_relation')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
