from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task, Workspace
from tasks.forms import (
    TaskCreateForm,
    TaskUpdateForm,
    )
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def task_list(request, pk):
    tasks = Task.objects.filter(workspace_id=pk)
    template_name = 'tasks/task_list.html'
    context = {'tasks':tasks}
    return render (request, template_name, context)

def save_task_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            tasks = Task.objects.filter(workspace_id=form.instance.workspace_id)
            data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html',
                {'tasks':tasks}
            )
        else:
            data['form_is_valid'] = False
    context = {'form':form}
    data['html_form'] = render_to_string(
        template_name,
        context,
        request=request,
    )
    return JsonResponse(data)

@login_required(login_url='login')
def task_create(request):
    data = dict()
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            # need workspace_id here
            task.save()
            data['form_is_valid'] = True
            tasks = Task.objects.all()
            data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html',
                {'tasks':tasks}
            )
        else:
            data['form_is_valid'] = False
    else:
        form = TaskCreateForm()
    context = {'form':form}
    data['html_form'] = render_to_string(
        'tasks/includes/partial_task_create.html',
        context,
        request=request,
    )
    return JsonResponse(data)

@login_required(login_url='login')
def task_update(request, pk):
    task = get_object_or_404(Task, task_id=pk)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
    else:
        form = TaskUpdateForm(instance=task)
    return save_task_form(request, form, 'tasks/includes/partial_task_update.html')

@login_required(login_url='login')
def task_delete(request, pk):
    task = get_object_or_404(Task, task_id=pk)
    data = dict()
    if request.method == "POST":
        task.delete()
        data['form_is_valid'] = True
        tasks = Task.objects.filter(workspace_id=pk)
        data['html_task_list'] = render_to_string('tasks/includes/partial_task_list.html',
                {'tasks':tasks}
            )
    else:
        context = {'task':task}
        data['html_form'] = render_to_string(
            'tasks/includes/partial_task_delete_confirm.html',
            context,
            request=request,
            )
    return JsonResponse(data)