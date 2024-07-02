from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tasks.models import Task, Workspace

# Create your views here.

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.all()
    template_name = 'workspace/task_list.html'
    context = {'tasks':tasks}
    return render (request, template_name, context)