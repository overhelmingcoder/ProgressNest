from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from .models import Group, GroupMembership, GroupPost, GroupPostComment
from .forms import GroupForm, GroupPostForm, GroupPostCommentForm

class GroupListView(ListView):
    model = Group
    template_name = 'groups/group_list.html'
    context_object_name = 'groups'
    paginate_by = 12

    def get_queryset(self):
        queryset = Group.objects.filter(is_active=True)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Privacy filter
        privacy = self.request.GET.get('privacy')
        if privacy:
            queryset = queryset.filter(privacy=privacy)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Group.CATEGORY_CHOICES
        context['privacy_options'] = Group.PRIVACY_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['current_privacy'] = self.request.GET.get('privacy', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class MyGroupsView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups/my_groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        user_memberships = GroupMembership.objects.filter(user=self.request.user, status='active')
        return Group.objects.filter(id__in=user_memberships.values_list('group_id', flat=True))

class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_detail.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.filter(is_approved=True)[:10]
        context['members'] = self.object.get_members()[:12]
        context['is_member'] = False
        context['membership'] = None
        
        if self.request.user.is_authenticated:
            try:
                context['membership'] = GroupMembership.objects.get(
                    group=self.object, user=self.request.user
                )
                context['is_member'] = context['membership'].status == 'active'
            except GroupMembership.DoesNotExist:
                pass
            
            context['post_form'] = GroupPostForm()
        
        return context

class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_form.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        
        # Automatically make creator a member
        GroupMembership.objects.create(
            group=self.object,
            user=self.request.user,
            role='admin',
            status='active'
        )
        
        messages.success(self.request, 'Group created successfully!')
        return response

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/group_form.html'

    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Group updated successfully!')
        return super().form_valid(form)

class GroupMembersView(DetailView):
    model = Group
    template_name = 'groups/group_members.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.get_members()
        return context

@login_required
def join_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    membership, created = GroupMembership.objects.get_or_create(
        group=group,
        user=request.user,
        defaults={
            'status': 'pending' if group.require_approval else 'active',
            'role': 'member'
        }
    )
    
    if created:
        if group.require_approval:
            messages.info(request, 'Your request to join has been sent for approval.')
        else:
            messages.success(request, f'You have joined {group.name}!')
            group.update_member_count()
    else:
        if membership.status == 'pending':
            messages.info(request, 'Your request is still pending approval.')
        elif membership.status == 'banned':
            messages.error(request, 'You are banned from this group.')
        else:
            messages.info(request, 'You are already a member of this group.')
    
    return redirect('groups:detail', slug=slug)

@login_required
def leave_group(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    try:
        membership = GroupMembership.objects.get(group=group, user=request.user)
        membership.delete()
        group.update_member_count()
        messages.success(request, f'You have left {group.name}.')
    except GroupMembership.DoesNotExist:
        messages.error(request, 'You are not a member of this group.')
    
    return redirect('groups:detail', slug=slug)

@login_required
def create_group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    
    if not group.can_post(request.user):
        messages.error(request, 'You do not have permission to post in this group.')
        return redirect('groups:detail', slug=slug)
    
    if request.method == 'POST':
        form = GroupPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.group = group
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('groups:detail', slug=slug)
    else:
        form = GroupPostForm()
    
    return render(request, 'groups/group_post_form.html', {'form': form, 'group': group})

@login_required
def like_group_post(request, pk):
    post = get_object_or_404(GroupPost, pk=pk)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.method == 'POST':
        return JsonResponse({
            'success': True,
            'liked': liked,
            'count': post.total_likes
        })
    
    return redirect('groups:detail', slug=post.group.slug)

@login_required
def add_group_post_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(GroupPost, pk=pk)
        form = GroupPostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    
    return redirect('groups:detail', slug=post.group.slug)
