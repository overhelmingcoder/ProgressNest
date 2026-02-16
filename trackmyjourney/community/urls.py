from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.CommunityListView.as_view(), name='list'),
    path('<int:pk>/', views.community_detail, name='detail'),
    path('<int:pk>/join/', views.join_community, name='join'),
    path('<int:community_pk>/create-post/', views.create_post, name='create_post'),
    path('post/<int:pk>/like/', views.toggle_like_post, name='toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark_post, name='toggle_bookmark'),
]

