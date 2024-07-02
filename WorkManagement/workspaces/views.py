from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workspaces.models import Workspace
from workspaces.forms import WorkspaceCreateForm

# Create your views here.

# @login_required(login_url='login')
def workspace_list(request):
    workspaces = Workspace.objects.all()
    template_name = 'workspace/workspace_list.html'
    context = {'workspaces':workspaces}
    return render (request, template_name, context)

def workspace_create(request):
    if request.method == "POST":
        form = WorkspaceCreateForm(request.POST)
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.save()
            # return JsonResponse(workspace)
        # 
    else:
        form = WorkspaceCreateForm()
    template_name = 'workspace/workspace_create.html'
    context = {'form':form}
    return render(request, template_name, context)

def workspace_delete(request, pk):
    workspaces = get_object_or_404(Workspace, workspace_id=pk)
    if request.method == "POST":
        workspaces.delete()
        return redirect ('workspace_list')
    template_name = 'workspace/workspace_delete.html'
    context = {'workspaces':workspaces}
    return render(request, template_name, context)