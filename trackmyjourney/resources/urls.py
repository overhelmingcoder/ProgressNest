from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.ResourceListView.as_view(), name='list'),
    path('create/', views.ResourceCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ResourceDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ResourceUpdateView.as_view(), name='update'), # Assuming you have update view
    path('<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='delete'), # Assuming you have delete view
    path('<int:pk>/download/', views.download_resource, name='download'),
    path('<int:pk>/comment/', views.add_resource_comment, name='add_comment'),
    path('<int:pk>/rate/', views.rate_resource, name='rate'),
    path('<int:pk>/like/', views.like_resource, name='like'), # Add this line
    path('<int:pk>/bookmark/', views.bookmark_resource, name='bookmark'), # Add this line
    path('my-uploads/', views.MyResourceListView.as_view(), name='my_list'), # Assuming you have a 'my_list' view
]