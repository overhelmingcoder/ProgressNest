from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Achievement(models.Model):
    CATEGORY_CHOICES = [
        ('goal', 'Goal Achievement'),
        ('milestone', 'Milestone'),
        ('habit', 'Habit Formation'),
        ('learning', 'Learning'),
        ('fitness', 'Fitness'),
        ('career', 'Career'),
        ('personal', 'Personal Development'),
        ('social', 'Social'),
        ('creative', 'Creative'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    badge_icon = models.CharField(max_length=50, default='fas fa-trophy')
    badge_color = models.CharField(max_length=7, default='#f59e0b')
    badge_type = models.CharField(max_length=50, default='default')  # Add this line
    date_achieved = models.DateField()
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_achieved', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('achievements:detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()

class AchievementLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} likes {self.achievement.title}"

class AchievementComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.achievement.title}"
