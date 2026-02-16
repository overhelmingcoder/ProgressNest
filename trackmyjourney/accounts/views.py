from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm
from .models import UserProfile

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    # Profile is created automatically via signals
                    login(request, user)
                    messages.success(request, f'Welcome to TrackMyJourney, {user.get_full_name()}! 🎉')
                    return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'There was an error creating your account. Please try again.')
                print(f"Signup error: {e}")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return '/dashboard/'
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().get_full_name()}! 👋')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

@login_required
def profile_view(request):
    # Ensure user has a profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your profile has been updated successfully! ✨')
                return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, 'There was an error updating your profile. Please try again.')
                print(f"Profile update error: {e}")
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Initialize context with safe defaults
        context.update({
            'profile': profile,
            'recent_goals': [],
            'recent_achievements': [],
            'recent_blog_posts': [],
            'recent_resources': [],
            'total_goals': 0,
            'completed_goals': 0,
            'in_progress_goals': 0,
            'total_achievements': 0,
            'total_blog_posts': 0,
            'total_resources': 0,
        })
        
        # Try to get data from other apps safely
        try:
            from goals.models import Goal
            goals = Goal.objects.filter(user=user)
            context['recent_goals'] = goals.order_by('-created_at')[:5]
            context['total_goals'] = goals.count()
            context['completed_goals'] = goals.filter(status='completed').count()
            context['in_progress_goals'] = goals.filter(status='in_progress').count()
            
            # Update profile stats
            profile.total_goals = context['total_goals']
            profile.completed_goals = context['completed_goals']
        except (ImportError, Exception):
            pass
        
        try:
            from achievements.models import Achievement
            achievements = Achievement.objects.filter(user=user)
            context['recent_achievements'] = achievements.order_by('-created_at')[:5]
            context['total_achievements'] = achievements.count()
            profile.total_achievements = context['total_achievements']
        except (ImportError, Exception):
            pass
        
        try:
            from blog.models import BlogPost
            posts = BlogPost.objects.filter(author=user)
            context['recent_blog_posts'] = posts.order_by('-created_at')[:3]
            context['total_blog_posts'] = posts.count()
            profile.total_blog_posts = context['total_blog_posts']
        except (ImportError, Exception):
            pass
        
        try:
            from resources.models import Resource
            resources = Resource.objects.filter(uploaded_by=user)
            context['recent_resources'] = resources.order_by('-uploaded_at')[:3]
            context['total_resources'] = resources.count()
            profile.total_resources = context['total_resources']
        except (ImportError, Exception):
            pass
        
        # Save updated profile stats
        try:
            profile.save()
        except Exception:
            pass
        
        return context

@login_required
def onboarding_view(request):
    """Optional onboarding flow for new users"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Check if user needs onboarding
    needs_onboarding = (
        profile.total_goals == 0 and 
        profile.total_achievements == 0 and 
        not request.user.bio
    )
    
    if needs_onboarding:
        return render(request, 'accounts/onboarding.html', {'profile': profile})
    else:
        return redirect('dashboard')
    
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

def edit_profile(request):
    # Your view logic here
    return render(request, 'accounts/edit_profile.html')