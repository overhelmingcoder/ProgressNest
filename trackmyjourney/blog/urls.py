from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Specific paths first
    path('my-posts/', views.MyBlogListView.as_view(), name='my_list'),
    path('create/', views.BlogCreateView.as_view(), name='create'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    
    # Generic slug patterns (after specific patterns)
    path('<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='delete'),
    path('<slug:slug>/like/', views.like_post, name='like'),
    path('<slug:slug>/bookmark/', views.bookmark_post, name='bookmark'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    
    # Root path last
    path('', views.BlogListView.as_view(), name='list'),
]
