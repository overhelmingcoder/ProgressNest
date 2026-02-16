from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Q
from django.utils import timezone
import json

# Import your models
from .models import Resource, ResourceComment, ResourceRating, ResourceLike, ResourceBookmark

# Import your forms
from .forms import ResourceForm, ResourceCommentForm, ResourceRatingForm


class ResourceListView(ListView):
    model = Resource
    template_name = 'resources/resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        queryset = Resource.objects.all()
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        resource_type = self.request.GET.get('type')

        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(tags__icontains=search))
        if category:
            queryset = queryset.filter(category=category)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset.order_by('-uploaded_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Resource.CATEGORY_CHOICES
        context['types'] = Resource.RESOURCE_TYPE_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'resources/resource_detail.html'
    context_object_name = 'resource'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.increment_views()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.tags:
            context['processed_tags'] = [tag.strip() for tag in self.object.tags.split(',')]
        else:
            context['processed_tags'] = []
        
        context['comments'] = ResourceComment.objects.filter(resource=self.object).order_by('-created_at')
        context['rating_form'] = ResourceRatingForm()
        context['comment_form'] = ResourceCommentForm()
        return context

class ResourceCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm # Use the imported form
    template_name = 'resources/resource_form.html'

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Resource uploaded successfully!')
        return super().form_valid(form)

class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm # Use the imported form
    template_name = 'resources/resource_form.html'

    def get_queryset(self):
        return Resource.objects.filter(uploaded_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Resource updated successfully!')
        return super().form_valid(form)

class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    template_name = 'resources/resource_confirm_delete.html'
    success_url = reverse_lazy('resources:list')

    def get_queryset(self):
        return Resource.objects.filter(uploaded_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Resource deleted successfully.')
        return super().delete(request, *args, **kwargs)

@login_required
def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if resource.file:
        resource.downloads += 1
        resource.save(update_fields=['downloads'])
        response = HttpResponse(resource.file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{resource.file.name}"'
        return response
    messages.error(request, 'No file available for download.')
    return redirect('resources:detail', pk=pk)

@login_required
def add_resource_comment(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('resources:detail', pk=pk)
    messages.error(request, 'Failed to add comment.')
    return redirect('resources:detail', pk=pk)

@login_required
def rate_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceRatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            review_content = form.cleaned_data.get('review', '')
            
            existing_rating = ResourceRating.objects.filter(user=request.user, resource=resource).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.review = review_content
                existing_rating.save()
                messages.info(request, 'Your rating has been updated!')
            else:
                ResourceRating.objects.create(
                    user=request.user,
                    resource=resource,
                    rating=rating_value,
                    review=review_content
                )
                messages.success(request, 'Thank you for your rating!')
            return redirect('resources:detail', pk=pk)
    messages.error(request, 'Failed to submit rating.')
    return redirect('resources:detail', pk=pk)

@login_required
def like_resource(request, pk):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=pk)
        user = request.user
        
        liked = False
        if ResourceLike.objects.filter(user=user, resource=resource).exists():
            ResourceLike.objects.filter(user=user, resource=resource).delete()
            messages.info(request, 'Resource unliked.')
        else:
            ResourceLike.objects.create(user=user, resource=resource)
            liked = True
            messages.success(request, 'Resource liked!')
        
        return JsonResponse({'status': 'success', 'liked': liked, 'total_likes': resource.resourcelike_set.count()})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def bookmark_resource(request, pk):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=pk)
        user = request.user
        
        bookmarked = False
        if ResourceBookmark.objects.filter(user=user, resource=resource).exists():
            ResourceBookmark.objects.filter(user=user, resource=resource).delete()
            messages.info(request, 'Resource unbookmarked.')
        else:
            ResourceBookmark.objects.create(user=user, resource=resource)
            bookmarked = True
            messages.success(request, 'Resource bookmarked!')
        
        return JsonResponse({'status': 'success', 'bookmarked': bookmarked, 'total_bookmarks': resource.resourcebookmark_set.count()})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


class MyResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = 'resources/my_resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12

    def get_queryset(self):
        return Resource.objects.filter(uploaded_by=self.request.user).order_by('-uploaded_at')
