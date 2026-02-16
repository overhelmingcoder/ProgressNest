from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.GoalListView.as_view(), name='list'),
    path('create/', views.GoalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.GoalDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.GoalUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.GoalDeleteView.as_view(), name='delete'),
     #path('<int:pk>/complete/', views.GoalCompleteView.as_view(), name='complete'),
    path('<int:pk>/update/', views.GoalUpdateView.as_view(), name='update'),


     #path('<int:goal_id>/milestones/', views.milestone_list, name='milestone_list'),
    path('<int:goal_id>/milestone/', views.add_milestone, name='add_milestone'),
    path('<int:goal_id>/progress/', views.update_progress, name='update_progress'),
    path('milestone/<int:milestone_id>/toggle/', views.toggle_milestone, name='toggle_milestone'),
]
