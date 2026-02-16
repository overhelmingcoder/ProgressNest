from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

# Assuming you have a Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    # ... other fields as per your project

    def __str__(self):
        return self.name

class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(auto_now_add=True)
    # Assuming 'end_date' in your template refers to 'target_date' from the form
    # If you have a separate 'end_date' field, adjust accordingly.
    end_date = models.DateField(null=True, blank=True) 
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # These fields will now be managed by the update_progress_and_status method
    progress = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('goals:detail', kwargs={'pk': self.pk})

    @property
    def days_remaining(self):
        if self.target_date and self.status != 'completed':
            today = timezone.localdate()
            remaining = (self.target_date - today).days
            return max(0, remaining)
        return 0

    @property
    def is_overdue(self):
        if self.target_date and self.status != 'completed':
            return timezone.localdate() > self.target_date
        return False

    def update_progress_and_status(self):
        """
        Calculates and updates the goal's progress and status based on its milestones.
        """
        total_milestones = self.milestones.count()
        completed_milestones = self.milestones.filter(is_completed=True).count()

        if total_milestones > 0:
            self.progress = int((completed_milestones / total_milestones) * 100)
        else:
            self.progress = 0 # No milestones, 0% progress

        # Update status based on progress
        if self.progress == 100 and total_milestones > 0:
            self.status = 'completed'
            if not self.completed_at: # Set completed_at only if it's not already set
                self.completed_at = timezone.now()
        elif self.progress > 0 and self.progress < 100:
            self.status = 'in_progress'
            self.completed_at = None # Clear completed_at if no longer 100%
        else: # progress is 0
            self.status = 'not_started'
            self.completed_at = None # Clear completed_at if no longer 100%

        # Save only the fields that were updated by this method
        self.save(update_fields=['progress', 'status', 'completed_at'])


class Milestone(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['target_date', 'created_at']

class GoalUpdate(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    progress_change = models.IntegerField(default=0) # e.g., +10, -5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.goal.title} by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']
