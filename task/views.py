from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm, CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.http import HttpResponse


User = get_user_model()


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-priority', '-created_at')

    # Apply filters
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')
    overdue_filter = request.GET.get('overdue')

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if overdue_filter == 'yes':
        tasks = tasks.filter(
            due_date__lt=timezone.now().date(),
            status__in=['pending', 'in_progress']
        )

    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
    }
    return render(request, 'tasks/home.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/add_task.html', {
        'form': form,
        'title': 'Add New Task',
        'button_text': 'Add Task'
    })


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/add_task.html', {
        'form': form,
        'title': 'Edit Task',
        'button_text': 'Update Task'
    })


@require_POST
@login_required
def quick_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_status = request.POST.get('status')
    new_priority = request.POST.get('priority')

    if new_status in [choice[0] for choice in Task.STATUS_CHOICES]:
        task.status = new_status

    if new_priority:
        try:
            task.priority = int(new_priority)
        except ValueError:
            pass

    task.save()
    messages.success(request, 'Task updated successfully!')
    return redirect('task_list')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 'Registration successful! Please log in.')
        return response


def ping_view(request):
    return HttpResponse("pong")








