from django.db import models
from django.contrib.auth.models import User

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class HomePageSettings(models.Model):
    """Settings for homepage content"""
    hero_title = models.CharField(max_length=200, default="Learn and Share")
    hero_subtitle = models.TextField(default="Learn practically and effectively with TrackMyJourney—a cybersecurity hub for tracking goals, documenting achievements, and sharing technical insights!")
    about_text = models.TextField(default="TrackMyJourney is a dedicated cybersecurity learning platform...")
    goal_text = models.TextField(default="Our goal is to bridge the gap between learning and practical application...")
    
    # Statistics
    users_count = models.IntegerField(default=20000)
    collaborations_count = models.IntegerField(default=300)
    
    # Contact info
    phone = models.CharField(max_length=20, default="+880 1925292827")
    email = models.EmailField(default="mahathir.khandaker.mk@mail.com")
    address = models.CharField(max_length=200, default="Chottogram, BD")
    
    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and HomePageSettings.objects.exists():
            raise ValueError('Only one HomePageSettings instance is allowed')
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

class FakePost(models.Model):
    """Fake posts for demo purposes until you integrate with real blog"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    tags = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
