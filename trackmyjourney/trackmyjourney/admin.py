from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

class TrackMyJourneyAdminSite(AdminSite):
    site_header = 'TrackMyJourney Administration'
    site_title = 'TrackMyJourney Admin'
    index_title = 'Welcome to TrackMyJourney Administration'
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Add custom dashboard data
        from django.contrib.auth import get_user_model
        from goals.models import Goal
        from achievements.models import Achievement
        from blog.models import BlogPost
        from resources.models import Resource
        from books.models import Book
        from groups.models import Group
        from community.models import Community
        
        User = get_user_model()
        
        extra_context.update({
            'total_users': User.objects.count(),
            'total_goals': Goal.objects.count(),
            'completed_goals': Goal.objects.filter(status='completed').count(),
            'total_achievements': Achievement.objects.count(),
            'total_posts': BlogPost.objects.count(),
            'published_posts': BlogPost.objects.filter(status='published').count(),
            'total_resources': Resource.objects.count(),
            'total_books': Book.objects.count(),
            'total_groups': Group.objects.count(),
            'total_communities': Community.objects.count(),
        })
        
        return super().index(request, extra_context)

admin_site = TrackMyJourneyAdminSite(name='trackmyjourney_admin')

# Register all models with custom admin site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User, UserProfile
from achievements.models import Achievement, AchievementComment
from blog.models import BlogPost, Category as BlogCategory, Comment as BlogComment
from books.models import Book, BookCategory, ReadingList, BookRating
from goals.models import Goal, Category as GoalCategory, Milestone, GoalUpdate
from resources.models import Resource, ResourceComment, ResourceRating
from groups.models import Group, GroupMembership, GroupPost, GroupPostComment
from community.models import Community, Post, CommunityMembership, PostLike, Comment as CommunityComment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

admin_site.register(User, CustomUserAdmin)
admin_site.register(UserProfile)

class AchievementCommentInline(admin.TabularInline):
    model = AchievementComment
    extra = 0

class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'badge_type', 'date_achieved', 'is_public', 'total_likes')
    list_filter = ('category', 'badge_type', 'is_public', 'date_achieved')
    search_fields = ('title', 'user__username')
    date_hierarchy = 'date_achieved'
    inlines = [AchievementCommentInline]

admin_site.register(Achievement, AchievementAdmin)
admin_site.register(AchievementComment)

class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'post_count', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'is_featured', 'views', 'total_likes', 'created_at')
    list_filter = ('status', 'is_featured', 'created_at', 'categories')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [BlogCommentInline]

admin_site.register(BlogCategory, BlogCategoryAdmin)
admin_site.register(BlogPost, BlogPostAdmin)
admin_site.register(BlogComment)

class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class BookRatingInline(admin.TabularInline):
    model = BookRating
    extra = 0

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded_by', 'format', 'language', 'is_public', 'downloads', 'views')
    list_filter = ('format', 'language', 'is_public', 'is_featured', 'uploaded_at')
    search_fields = ('title', 'author', 'isbn', 'uploaded_by__username')
    date_hierarchy = 'uploaded_at'
    inlines = [BookRatingInline]

admin_site.register(BookCategory, BookCategoryAdmin)
admin_site.register(Book, BookAdmin)
admin_site.register(ReadingList)
admin_site.register(BookRating)

class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0

class GoalUpdateInline(admin.TabularInline):
    model = GoalUpdate
    extra = 0
    readonly_fields = ['created_at']

class GoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'priority', 'progress', 'target_date', 'created_at']
    list_filter = ['status', 'priority', 'category', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    inlines = [MilestoneInline, GoalUpdateInline]

class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'goal', 'target_date', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'target_date', 'created_at']

admin_site.register(GoalCategory, GoalCategoryAdmin)
admin_site.register(Goal, GoalAdmin)
admin_site.register(Milestone, MilestoneAdmin)
admin_site.register(GoalUpdate)

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'category', 'resource_type', 'is_public', 'downloads', 'views', 'uploaded_at')
    list_filter = ('category', 'resource_type', 'is_public', 'is_featured', 'uploaded_at')
    search_fields = ('title', 'uploaded_by__username', 'description')
    date_hierarchy = 'uploaded_at'

admin_site.register(Resource, ResourceAdmin)
admin_site.register(ResourceComment)
admin_site.register(ResourceRating)

class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0

class GroupPostCommentInline(admin.TabularInline):
    model = GroupPostComment
    extra = 0

class GroupPostInline(admin.TabularInline):
    model = GroupPost
    extra = 0

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'category', 'privacy', 'member_count', 'created_at')
    list_filter = ('category', 'privacy', 'is_active', 'created_at')
    search_fields = ('name', 'creator__username')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    inlines = [GroupMembershipInline]

class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'author', 'is_pinned', 'created_at')
    list_filter = ('group', 'is_pinned', 'created_at')
    search_fields = ('title', 'author__username')
    inlines = [GroupPostCommentInline]

admin_site.register(Group, GroupAdmin)
admin_site.register(GroupMembership)
admin_site.register(GroupPost, GroupPostAdmin)
admin_site.register(GroupPostComment)

class PostCommentInline(admin.TabularInline):
    model = CommunityComment
    extra = 0

class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'community', 'created_at')
    list_filter = ('community', 'created_at')
    search_fields = ('title', 'author__username')
    inlines = [PostCommentInline]

class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_featured', 'created_at')
    list_filter = ('category', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ['created_at']

admin_site.register(Community, CommunityAdmin)
admin_site.register(Post, CommunityPostAdmin)
admin_site.register(CommunityMembership)
admin_site.register(PostLike)
admin_site.register(CommunityComment)
