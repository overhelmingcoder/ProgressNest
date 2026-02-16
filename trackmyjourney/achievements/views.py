from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from .models import Achievement, AchievementComment, AchievementLike
from .forms import AchievementForm, CommentForm

class AchievementListView(LoginRequiredMixin, ListView):
    model = Achievement
    template_name = 'achievements/achievement_list.html'
    context_object_name = 'achievements'
    paginate_by = 12

    def get_queryset(self):
        queryset = Achievement.objects.filter(user=self.request.user)
        category = self.request.GET.get('category')
        badge = self.request.GET.get('badge')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if badge:
            queryset = queryset.filter(badge_type=badge)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for ach in context.get('achievements', []):
            ach.liked_by = ach.is_liked_by(user) if user.is_authenticated else False
        return context

class PublicAchievementListView(ListView):
    model = Achievement
    template_name = 'achievements/public_achievements.html'
    context_object_name = 'achievements'
    paginate_by = 12

    def get_queryset(self):
        queryset = Achievement.objects.filter(is_public=True)
        category = self.request.GET.get('category')
        badge = self.request.GET.get('badge')
        search = self.request.GET.get('search')
        
        if category:
            queryset = queryset.filter(category=category)
        if badge:
            queryset = queryset.filter(badge_type=badge)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        for ach in context.get('achievements', []):
            ach.liked_by = ach.is_liked_by(user) if user.is_authenticated else False
        return context

class AchievementDetailView(DetailView):
    model = Achievement
    template_name = 'achievements/achievement_detail.html'
    context_object_name = 'achievement'

    def get_queryset(self):
        queryset = Achievement.objects.all()
        # If user is not authenticated, only show public achievements
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_public=True)
        # If user is authenticated, show their own achievements and all public achievements
        else:
            queryset = queryset.filter(
                Q(user=self.request.user) | Q(is_public=True)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        user = self.request.user
        context['is_liked'] = self.object.is_liked_by(user) if user.is_authenticated else False
        return context

class AchievementCreateView(LoginRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Achievement created successfully!')
        return super().form_valid(form)

class AchievementUpdateView(LoginRequiredMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Achievement updated successfully!')
        return super().form_valid(form)

class AchievementDeleteView(LoginRequiredMixin, DeleteView):
    model = Achievement
    template_name = 'achievements/achievement_confirm_delete.html'
    success_url = reverse_lazy('achievements:list')

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Achievement deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def like_achievement(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    
    # Check if user has already liked
    like_obj = AchievementLike.objects.filter(user=request.user, achievement=achievement).first()
    
    if like_obj:
        like_obj.delete()
        liked = False
    else:
        AchievementLike.objects.create(user=request.user, achievement=achievement)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'POST':
        return JsonResponse({
            'success': True,
            'liked': liked,
            'count': achievement.total_likes()
        })
    
    return redirect('achievements:detail', pk=pk)

@login_required
def add_comment(request, pk):
    achievement = get_object_or_404(Achievement, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.achievement = achievement
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    
    return redirect('achievements:detail', pk=pk)
