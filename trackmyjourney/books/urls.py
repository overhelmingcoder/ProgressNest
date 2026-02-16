from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Specific paths first (before generic slug patterns)
    path('upload/', views.BookCreateView.as_view(), name='create'),
    path('reading-list/', views.ReadingListView.as_view(), name='reading_list'),
    path('reading-list/add/<slug:slug>/', views.add_to_reading_list, name='add_to_reading_list'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),
    path('categories/', views.BookCategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', views.BookCategoryDetailView.as_view(), name='category_detail'),
    
    # Generic slug patterns (after specific patterns)
    path('<slug:slug>/edit/', views.BookUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.BookDeleteView.as_view(), name='delete'),
    path('<slug:slug>/download/', views.download_book, name='download'),
    path('<slug:slug>/like/', views.like_book, name='like'),
    path('<slug:slug>/bookmark/', views.bookmark_book, name='bookmark'),
    path('<slug:slug>/rate/', views.rate_book, name='rate'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
    
    # Root path last
    path('', views.BookListView.as_view(), name='list'),
]
