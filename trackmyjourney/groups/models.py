from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class Group(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('invite_only', 'Invite Only'),
    ]
    
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('programming', 'Programming'),
        ('data-science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('ai-ml', 'AI & Machine Learning'),
        ('web-dev', 'Web Development'),
        ('mobile-dev', 'Mobile Development'),
        ('career', 'Career & Professional'),
        ('education', 'Education & Learning'),
        ('research', 'Research & Academia'),
        ('startup', 'Startup & Business'),
        ('design', 'Design & UX'),
        ('health-tech', 'Health Technology'),
        ('fintech', 'Financial Technology'),
        ('gaming', 'Gaming & Entertainment'),
        ('open-source', 'Open Source'),
        ('networking', 'Professional Networking'),
        ('mentorship', 'Mentorship'),
        ('study-group', 'Study Groups'),
        ('project-collab', 'Project Collaboration'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    privacy = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    cover_image = models.ImageField(upload_to='groups/covers/', blank=True, null=True)
    logo = models.ImageField(upload_to='groups/logos/', blank=True, null=True)
    rules = models.TextField(blank=True, help_text="Group rules and guidelines")
    tags = models.CharField(max_length=200, blank=True)
    
    # Group management
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    admins = models.ManyToManyField(User, related_name='admin_groups', blank=True)
    moderators = models.ManyToManyField(User, related_name='moderated_groups', blank=True)
    
    # Settings
    allow_member_posts = models.BooleanField(default=True)
    require_approval = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Stats
    member_count = models.PositiveIntegerField(default=0)
    post_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('groups:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Group.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_members(self):
        return GroupMembership.objects.filter(group=self, status='active')
    
    def update_member_count(self):
        self.member_count = self.get_members().count()
        self.save(update_fields=['member_count'])
    
    def is_admin(self, user):
        return user == self.creator or user in self.admins.all()
    
    def is_moderator(self, user):
        return self.is_admin(user) or user in self.moderators.all()
    
    def is_member(self, user):
        return GroupMembership.objects.filter(group=self, user=user, status='active').exists()
    
    def can_post(self, user):
        if not user.is_authenticated:
            return False
        if self.is_moderator(user):
            return True
        if not self.allow_member_posts:
            return False
        return self.is_member(user)

class GroupMembership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending Approval'),
        ('banned', 'Banned'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='group_invitations'
    )

    class Meta:
        unique_together = ['group', 'user']

    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"

class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='groups/posts/', blank=True, null=True)
    file = models.FileField(upload_to='groups/files/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_group_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} in {self.group.name}"
    
    @property
    def total_likes(self):
        return self.likes.count()

class GroupPostComment(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_group_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
