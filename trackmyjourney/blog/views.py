from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import BlogPost, Category, Comment
from .forms import BlogPostForm, CommentForm

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published')
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(categories__slug=category)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) | 
                Q(tags__icontains=search)
            )
            
        return queryset.distinct().order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_posts'] = BlogPost.objects.filter(
            status='published', is_featured=True
        ).order_by('-published_at')[:3]
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self):
        obj = get_object_or_404(BlogPost, slug=self.kwargs['slug'], status='published')
        # Increment view count
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_approved=True, parent=None)
        context['related_posts'] = BlogPost.objects.filter(
            categories__in=self.object.categories.all(),
            status='published'
        ).exclude(pk=self.object.pk).distinct()[:3]
        return context

class MyBlogListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/my_blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user).order_by('-created_at')

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published':
            form.instance.published_at = timezone.now()
        
        # Save the post first
        response = super().form_valid(form)
        
        # Update category post counts
        for category in self.object.categories.all():
            category.update_post_count()
        
        messages.success(self.request, 'Blog post created successfully!')
        return response

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.published_at:
            form.instance.published_at = timezone.now()
        
        response = super().form_valid(form)
        
        # Update category post counts
        for category in self.object.categories.all():
            category.update_post_count()
        
        messages.success(self.request, 'Blog post updated successfully!')
        return response

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:my_list')

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Update category post counts before deletion
        for category in self.get_object().categories.all():
            category.update_post_count()
        
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def like_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.total_likes
        })
    
    return redirect('blog:detail', slug=slug)

@login_required
def bookmark_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
        bookmarked = False
    else:
        post.bookmarks.add(request.user)
        bookmarked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'bookmarked': bookmarked,
            'total_bookmarks': post.total_bookmarks
        })
    
    return redirect('blog:detail', slug=slug)

@login_required
def add_comment(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    
    if not post.allow_comments:
        messages.error(request, 'Comments are disabled for this post.')
        return redirect('blog:detail', slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    
    return redirect('blog:detail', slug=slug)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': comment.total_likes
        })
    
    return redirect('blog:detail', slug=comment.post.slug)


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost
from django.http import Http404




class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self):
        slug = self.kwargs['slug']
        try:
            obj = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            raise Http404("No BlogPost matches the given query.")

        # Check permissions:
        # 1. If the post is published, it's publicly accessible.
        # 2. If the user is authenticated AND is the author of the post, they can view it regardless of status.
        if obj.status == 'published' or (self.request.user.is_authenticated and obj.author == self.request.user):
            # Increment view count only if it's a published post being viewed (publicly or by author)
            # or if it's a public user viewing any post (though the first condition handles published for public)
            if obj.status == 'published': # Only increment views for published posts
                obj.views += 1
                obj.save(update_fields=['views'])
            return obj
        else:
            # If not published and not the author, raise 404
            raise Http404("No BlogPost matches the given query.")
