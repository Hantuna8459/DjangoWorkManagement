from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workspaces.models import Workspace
from workspaces.forms import WorkspaceCreateForm

# Create your views here.

@login_required(login_url='login')
def workspace_list(request):
    workspaces = Workspace.objects.filter(user = request.user)
    template_name = 'workspaces/workspace_list.html'
    context = {'workspaces':workspaces}
    return render (request, template_name, context)

@login_required(login_url='login')
def workspace_create(request):
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.save()
            return redirect ('workspace_list')
    else:
        form = WorkspaceCreateForm()
    template_name = 'workspaces/workspace_create.html'
    context = {'form':form}
    return render(request, template_name, context)

@login_required(login_url='login')
def workspace_update(request, pk):
    workspace = get_object_or_404(Workspace, workspace_id=pk)
    if request.method == 'POST':
        form = WorkspaceCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workspace title change successfully!')
    else:
        form = WorkspaceCreateForm(instance=workspace)
    tempate_name = 'workspaces/workspace_update.html'
    context = {'form':form}
    return render(request, tempate_name, context)

@login_required(login_url='login')
def workspace_delete(request, pk):
    workspaces = get_object_or_404(Workspace, workspace_id=pk)
    if request.method == "POST":
        workspaces.delete()
        return redirect ('workspace_list')  
    template_name = 'workspaces/workspace_delete.html'
    context = {'workspaces':workspaces}
    return render(request, template_name, context)