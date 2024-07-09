from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Workspace
from tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
    )
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(workspace = request.workspace)
    template_name = 'workspaces/task_list.html'
    context = {'tasks':tasks}
    return render (request, template_name, context)

@login_required(login_url='login')
def task_create(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.workspace = request.workspace
            task.save()
            return redirect('task_list')
    else:
        form = TaskCreateForm()
    template = 'workspaces/task_create.html'
    context = {'form':form}
    return render(request, template, context)

@login_required(login_url='login')
def task_update(request, pk):
    task = get_object_or_404(Task, task_id=pk)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Task successfully!')
    else:
        form = TaskUpdateForm()
    tempate_name = 'workspaces/task_update.html'
    context = {'form':form}
    return render(request, tempate_name, context)

@login_required(login_url='login')
def task_delete(request, pk):
    tasks = get_object_or_404(Task, task_id=pk)
    if request.method == "POST":
        tasks.delete()
        return redirect ('task_list')
    template_name = 'workspaces/task_delete.html'
    context = {'tasks':tasks}
    return render(request, template_name, context)