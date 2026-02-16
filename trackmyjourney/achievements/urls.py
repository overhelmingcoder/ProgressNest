from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    # Specific paths first
    path('public/', views.PublicAchievementListView.as_view(), name='public'),
    path('create/', views.AchievementCreateView.as_view(), name='create'),
    
    # Generic pk patterns (after specific patterns)
    path('<int:pk>/edit/', views.AchievementUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AchievementDeleteView.as_view(), name='delete'),
    path('<int:pk>/like/', views.like_achievement, name='like'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/', views.AchievementDetailView.as_view(), name='detail'),
    
    # Root path last
    path('', views.AchievementListView.as_view(), name='list'),
]
