from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import ContactMessage, HomePageSettings, FakePost
import json

def home(request):
    """Homepage view"""
    # Get homepage settings
    settings = HomePageSettings.get_settings()
    
    # Get recent fake posts (replace with real posts later)
    recent_posts = FakePost.objects.all()[:6]
    
    context = {
        'settings': settings,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'home.html', context)

@require_POST
def contact(request):
    """Handle contact form submission"""
    try:
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required.'
                })
            messages.error(request, 'All fields are required.')
            return redirect('homepage:home')
        
        # Save contact message
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We\'ll get back to you soon.'
            })
        
        messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
        return redirect('homepage:home')
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('homepage:home')
