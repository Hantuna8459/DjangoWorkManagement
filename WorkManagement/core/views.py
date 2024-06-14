from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import(
    CustomRegisterForm, 
    CustomLoginForm,
)
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string

# Create your views here.

def login_view(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        username_or_email = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')       
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('workspace')
    template_name = 'auth/login.html'
    context = {'form':form}
    return render(request, template_name, context)

def register_view(request):
    form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect ('')
    else:
        form = CustomRegisterForm()
    template_name = 'auth/register.html'
    context = {'form':form}
    return render (request, template_name, context)

def email_verify_view(request):
    return render()

def password_reset_view(request):
    template_name = 'auth/password_reset.html'
    return render(request, template_name)

@login_required(login_url='login')
def workspace_view(request):
    template_name = 'workspace/workspace.html'
    return render (request, template_name)

@login_required(login_url='login')
def task_view():
    return render ()
