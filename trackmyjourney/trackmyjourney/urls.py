from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import DashboardView
from django.views.generic import TemplateView
from trackmyjourney.admin import admin_site




urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('homepage.urls')),

    
    #path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('goals/', include('goals.urls')),
    path('achievements/', include('achievements.urls')),
    path('blog/', include('blog.urls')),
    path('resources/', include('resources.urls')),
    path('books/', include('books.urls')),
    path('groups/', include('groups.urls')),
    path('community/', include('community.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
