from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from .models import Goal, Milestone, Category, GoalUpdate
from .forms import GoalForm, MilestoneForm, ProgressUpdateForm

class GoalListView(LoginRequiredMixin, ListView):
  model = Goal
  template_name = 'goals/goal_list.html'
  context_object_name = 'goals'
  paginate_by = 12

  def get_queryset(self):
      queryset = Goal.objects.filter(user=self.request.user)
      
      # Filter by status
      status = self.request.GET.get('status')
      if status and status != '':
          queryset = queryset.filter(status=status)
      
      # Filter by category - use category name instead of ID
      category = self.request.GET.get('category')
      if category and category != '':
          queryset = queryset.filter(category__name__iexact=category)
      
      # Search
      search = self.request.GET.get('search')
      if search and search.strip():
          queryset = queryset.filter(
              Q(title__icontains=search) | Q(description__icontains=search)
          )
      
      return queryset.order_by('-created_at')

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['categories'] = Category.objects.all()
      context['status_choices'] = Goal.STATUS_CHOICES
      context['status_filter'] = self.request.GET.get('status', '')
      context['category_filter'] = self.request.GET.get('category', '')
      context['search_query'] = self.request.GET.get('search', '')
      return context

class GoalDetailView(LoginRequiredMixin, DetailView):
  model = Goal
  template_name = 'goals/goal_detail.html'
  context_object_name = 'goal'

  def get_queryset(self):
      return Goal.objects.filter(user=self.request.user)

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['milestones'] = self.object.milestones.all()
      context['completed_milestones_count'] = self.object.milestones.filter(is_completed=True).count()
      context['updates'] = self.object.updates.all()[:10]
      context['milestone_form'] = MilestoneForm()
      context['progress_form'] = ProgressUpdateForm()
      return context

class GoalCreateView(LoginRequiredMixin, CreateView):
  model = Goal
  form_class = GoalForm
  template_name = 'goals/goal_form.html'

  def form_valid(self, form):
      form.instance.user = self.request.user
      messages.success(self.request, 'Goal created successfully! 🎯')
      return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
  model = Goal
  form_class = GoalForm
  template_name = 'goals/goal_form.html'

  def get_queryset(self):
      return Goal.objects.filter(user=self.request.user)

  def form_valid(self, form):
      messages.success(self.request, 'Goal updated successfully! ✨')
      return super().form_valid(form)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
  model = Goal
  template_name = 'goals/goal_confirm_delete.html'
  success_url = reverse_lazy('goals:list')

  def get_queryset(self):
      return Goal.objects.filter(user=self.request.user)

  def delete(self, request, *args, **kwargs):
      messages.success(request, 'Goal deleted successfully.')
      return super().delete(request, *args, **kwargs)

@login_required
def add_milestone(request, goal_id):
  goal = get_object_or_404(Goal, id=goal_id, user=request.user)
  
  if request.method == 'POST':
      form = MilestoneForm(request.POST)
      if form.is_valid():
          milestone = form.save(commit=False)
          milestone.goal = goal
          milestone.save()
          goal.update_progress_and_status() # Call the new method here
          messages.success(request, 'Milestone added successfully! 🎯')
          return redirect('goals:detail', pk=goal.pk)
  else:
      form = MilestoneForm()

  return render(request, 'goals/milestone_form.html', {'form': form, 'goal': goal})

@login_required
def update_progress(request, goal_id):
  goal = get_object_or_404(Goal, id=goal_id, user=request.user)
  
  if request.method == 'POST':
      form = ProgressUpdateForm(request.POST)
      if form.is_valid():
          update = form.save(commit=False)
          update.goal = goal
          update.user = request.user
          update.save()
          
          # The direct progress update below is for manual progress changes.
          # If you want progress to ONLY be based on milestones, remove or adjust this.
          # For now, we'll keep it and then ensure milestone-based progress is also reflected.
          goal.progress = max(0, min(100, goal.progress + update.progress_change))
          # The status update here is also for manual progress.
          # The update_progress_and_status method will handle overall status based on milestones.
          if goal.progress == 100 and goal.status != 'completed':
              goal.status = 'completed'
              goal.completed_at = timezone.now()
          goal.save() # Save the manual progress and status update
          
          goal.update_progress_and_status() # Recalculate based on milestones after manual update
          
          messages.success(request, 'Progress updated successfully! 📈')
          return redirect('goals:detail', pk=goal.pk)
  
  return redirect('goals:detail', pk=goal.pk)

@login_required
def toggle_milestone(request, milestone_id):
  milestone = get_object_or_404(Milestone, id=milestone_id, goal__user=request.user)
  
  milestone.is_completed = not milestone.is_completed
  if milestone.is_completed:
      milestone.completed_at = timezone.now()
  else:
      milestone.completed_at = None
  milestone.save()
  
  milestone.goal.update_progress_and_status() # Call the new method here
  
  messages.success(request, f'Milestone {"completed" if milestone.is_completed else "reopened"}! ✅')
  return redirect('goals:detail', pk=milestone.goal.pk)
