from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workspaces.models import Workspace
from workspaces.forms import (
    WorkspaceCreateForm,
    WorkspaceUpdateForm,
)

# Create your views here.

@login_required(login_url='login')
def workspace_list(request):
    workspaces = Workspace.objects.filter(user = request.user)
    template_name = 'workspaces/workspace_list.html'
    context = {'workspaces':workspaces}
    return render (request, template_name, context)

def save_workspace_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            workspace = form.save(commit=False)
            workspace.user = request.user
            workspace.save()
            data['form_is_valid'] = True
            workspaces = Workspace.objects.filter(user=request.user)
            data['html_workspace_list'] = render_to_string('workspaces/includes/partial_workspace_list.html',
                {'workspaces':workspaces}
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
def workspace_create(request):
    if request.method == 'POST':
        form = WorkspaceCreateForm(request.POST)
    else:
        form = WorkspaceCreateForm()
    return save_workspace_form(request, form, 'workspaces/includes/partial_workspace_create.html')
    
@login_required(login_url='login')
def workspace_update(request, pk):
    workspace = get_object_or_404(Workspace, workspace_id=pk)
    if request.method == 'POST':
        form = WorkspaceUpdateForm(request.POST, instance=workspace)
    else:
        form = WorkspaceUpdateForm(instance=workspace)
    return save_workspace_form(request, form, 'workspaces/includes/partial_workspace_update.html')

@login_required(login_url='login')
def workspace_delete(request, pk):
    workspace = get_object_or_404(Workspace, workspace_id=pk)
    data = dict()
    if request.method == "POST":
        workspace.delete()
        data['form_is_valid'] = True
        workspaces = Workspace.objects.filter(user=request.user)
        data['html_workspace_list'] = render_to_string('workspaces/partial_workspace_list.html',
            {'workspaces':workspaces}
        )
    else:
        context = {'workspace':workspace}
        data['html_form'] = render_to_string(
            'workspaces/includes/partial_workspace_delete_confirm.html',
            context,
            request=request,
        )
    return JsonResponse(data)