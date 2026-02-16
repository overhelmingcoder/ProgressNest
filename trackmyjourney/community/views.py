from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Community, Post, CommunityMembership, PostLike
from .forms import PostForm, CommunityForm
from blog.models import BlogPost as Post
  # Assuming you have a blog app
import json

class CommunityListView(ListView):
    model = Community
    template_name = 'community/community_list.html'
    context_object_name = 'communities'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Community.objects.annotate(
            member_count=Count('members'),
            post_count=Count('posts')
        )
        
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset.order_by('-is_featured', '-created_at')

def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    
    # Check if user is a member
    is_member = False
    is_moderator = False
    if request.user.is_authenticated:
        membership = CommunityMembership.objects.filter(
            user=request.user, 
            community=community
        ).first()
        is_member = membership is not None
        is_moderator = membership.is_moderator if membership else False
    
    # Get posts with search functionality
    search_query = request.GET.get('search', '')
    posts = community.posts.select_related('author').prefetch_related('likes', 'comments')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    
    # Paginate posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    # Get recent members
    recent_members = community.members.order_by('-communitymembership__joined_at')[:10]
    
    # Add user interaction data to posts
    if request.user.is_authenticated:
        for post in posts_page:
            post.is_liked = post.likes.filter(id=request.user.id).exists()
            post.is_bookmarked = post.bookmarks.filter(id=request.user.id).exists()
    
    context = {
        'community': community,
        'posts': posts_page,
        'recent_members': recent_members,
        'is_member': is_member,
        'is_moderator': is_moderator,
        'search_query': search_query,
        'post_form': PostForm() if is_member else None,
    }
    
    return render(request, 'community/community_detail.html', context)

@login_required
@require_POST
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    membership, created = CommunityMembership.objects.get_or_create(
        user=request.user,
        community=community
    )
    
    if created:
        message = f'You have joined {community.name}!'
        joined = True
    else:
        membership.delete()
        message = f'You have left {community.name}.'
        joined = False
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'joined': joined,
            'member_count': community.member_count,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('community:detail', pk=pk)

@login_required
def create_post(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    
    # Check if user is a member
    if not CommunityMembership.objects.filter(user=request.user, community=community).exists():
        messages.error(request, 'You must be a member to post in this community.')
        return redirect('community:detail', pk=community_pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.community = community
            post.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Post created successfully!',
                    'post_id': post.id
                })
            
            messages.success(request, 'Post created successfully!')
            return redirect('community:detail', pk=community_pk)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'community': community,
    }
    
    return render(request, 'community/create_post.html', context)

@login_required
@require_POST
def toggle_like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'success': True,
        'liked': liked,
        'like_count': post.like_count
    })

@login_required
@require_POST
def toggle_bookmark_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    
    return JsonResponse({
        'success': True,
        'bookmarked': bookmarked
    })

def home(request):
    """Home page view with recent posts and community data"""
    
    # Get recent posts (limit to 6 for the slider)
    recent_posts = Post.objects.select_related('author').prefetch_related('tags').order_by('-created_at')[:6]
    
    # Add tags_list property to each post for template
    for post in recent_posts:
        if hasattr(post, 'tags') and post.tags:
            post.tags_list = [tag.strip() for tag in post.tags.split(',') if tag.strip()]
        else:
            post.tags_list = []
    
    # Get featured communities (optional)
    featured_communities = Community.objects.filter(is_featured=True)[:3]
    
    context = {
        'recent_posts': recent_posts,
        'featured_communities': featured_communities,
    }
    
    return render(request, 'home.html', context)

@require_POST
def contact(request):
    """Handle contact form submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can add logic to save to database or send email
        # For now, we'll just show a success message
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We\'ll get back to you soon.'
            })
        
        messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
        return redirect('home')
    
    return redirect('home')

@login_required
def dashboard(request):
    """User dashboard view"""
    return render(request, 'dashboard.html')
