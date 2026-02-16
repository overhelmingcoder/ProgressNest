from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Q
from .models import Book, BookCategory, ReadingList, BookRating
from .forms import BookForm, BookRatingForm

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = Book.objects.filter(is_public=True)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(categories__slug=category)
        
        # Format filter
        format_filter = self.request.GET.get('format')
        if format_filter:
            queryset = queryset.filter(format=format_filter)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        context['formats'] = Book.FORMAT_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['current_format'] = self.request.GET.get('format', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class BookCategoryListView(ListView):
    model = BookCategory
    template_name = 'books/category_list.html'
    context_object_name = 'categories'

class BookCategoryDetailView(DetailView):
    model = BookCategory
    template_name = 'books/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.filter(is_public=True)
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_rating'] = BookRating.objects.filter(
                book=self.object, user=self.request.user
            ).first()
            context['rating_form'] = BookRatingForm()
            context['reading_list_item'] = ReadingList.objects.filter(
                book=self.object, user=self.request.user
            ).first()
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Book uploaded successfully!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def get_queryset(self):
        return Book.objects.filter(uploaded_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:my_books')

    def get_queryset(self):
        return Book.objects.filter(uploaded_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ReadingListView(LoginRequiredMixin, ListView):
    model = ReadingList
    template_name = 'books/reading_list.html'
    context_object_name = 'reading_list'

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

class MyBooksView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/my_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.filter(uploaded_by=self.request.user)

@login_required
def download_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if not book.is_public and book.uploaded_by != request.user:
        raise Http404("Book not found")
    
    if not book.allow_download:
        messages.error(request, 'This book is not available for download.')
        return redirect('books:detail', slug=slug)
    
    if book.file:
        book.increment_downloads()
        response = HttpResponse(book.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{book.file.name}"'
        return response
    else:
        messages.error(request, 'No file available for download.')
        return redirect('books:detail', slug=slug)

@login_required
def like_book(request, slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=slug)
        if request.user in book.likes.all():
            book.likes.remove(request.user)
            liked = False
        else:
            book.likes.add(request.user)
            liked = True
        return JsonResponse({'status': 'success', 'liked': liked, 'total_likes': book.total_likes})
    return JsonResponse({'status': 'error'})

@login_required
def bookmark_book(request, slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=slug)
        if request.user in book.bookmarks.all():
            book.bookmarks.remove(request.user)
            bookmarked = False
        else:
            book.bookmarks.add(request.user)
            bookmarked = True
        return JsonResponse({'status': 'success', 'bookmarked': bookmarked, 'total_bookmarks': book.total_bookmarks})
    return JsonResponse({'status': 'error'})

@login_required
def rate_book(request, slug):
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=slug)
        form = BookRatingForm(request.POST)
        if form.is_valid():
            rating, created = BookRating.objects.get_or_create(
                book=book,
                user=request.user,
                defaults={'rating': form.cleaned_data['rating'], 'review': form.cleaned_data['review']}
            )
            if not created:
                rating.rating = form.cleaned_data['rating']
                rating.review = form.cleaned_data['review']
                rating.save()
            messages.success(request, 'Rating submitted successfully!')
        else:
            messages.error(request, 'Error submitting rating.')
    return redirect('books:detail', slug=slug)

@login_required
def add_to_reading_list(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    reading_item, created = ReadingList.objects.get_or_create(
        book=book,
        user=request.user,
        defaults={'status': 'want_to_read'}
    )
    
    if created:
        messages.success(request, f'"{book.title}" added to your reading list!')
    else:
        messages.info(request, f'"{book.title}" is already in your reading list.')
    
    return redirect('books:detail', slug=slug)
