from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.GroupListView.as_view(), name='list'),
    path('my-groups/', views.MyGroupsView.as_view(), name='my_groups'),
    path('create/', views.GroupCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.GroupDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.GroupUpdateView.as_view(), name='update'),
    path('<slug:slug>/members/', views.GroupMembersView.as_view(), name='members'),
    path('<slug:slug>/join/', views.join_group, name='join'),
    path('<slug:slug>/leave/', views.leave_group, name='leave'),
    path('<slug:slug>/post/create/', views.create_group_post, name='create_post'),
    path('post/<int:pk>/like/', views.like_group_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_group_post_comment, name='add_comment'),
]
