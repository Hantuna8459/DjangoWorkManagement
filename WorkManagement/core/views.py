from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import(
    CustomRegisterForm, 
    CustomLoginForm,
    EmailVerifyForm,
    # Experiment
    EmailForm,
    OTPForm,
)
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import (
    Workspace,
    CustomUser,
    Task,
)
import pyotp
import time

# Create your views here.

# create OTP
def generate_otp():
    base32_secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32_secret, interval=300)
    otp = totp.now()
    return otp, base32_secret

def login_view(request):
    form = CustomLoginForm() 
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']     
            user = authenticate(request, username=username, password=password)
            login_save = request.POST.get('login_save')# manual set cookie expire age
            if user is not None:
                if user.is_active == True:
                    login(request, user)
                    if login_save:
                        request.session.set_expiry(1000000)
                        return redirect('workspace')
                    else:
                        request.session.set_expiry(0)
                    return redirect('workspace') 
    template_name = 'auth/login.html'
    context = {'form':form}
    return render(request, template_name, context)

def register(request):
    form = CustomRegisterForm()
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # send OTP
            otp, base32_secret = generate_otp()
            
            # store the data in the session
            request.session['base32_secret'] = base32_secret
            request.session['otp_timestamp'] = int(time.time())
            request.session['username'] = form.cleaned_data['username']
            request.session['email'] = form.cleaned_data['email']
            request.session['password'] = form.cleaned_data['password1']
            
            # send email
            subject = "noreply"
            message = render_to_string('auth/email_template.html', {
                'otp': otp,
                'user':user,
                })
            recipient_email = form.cleaned_data['email']
            send_mail(subject,
                      message,
                      from_email=('noreply@mail.com'),
                      recipient_list = [recipient_email],
                      fail_silently=False,
                      )
            return redirect('email_verification')
        else:
            messages.error(request, 'Email send failed!')
    else:
        form = CustomRegisterForm()
    template_name = 'auth/register.html'
    context = {'form':form}
    return render (request, template_name, context)

def email_verify(request):
        form = EmailVerifyForm()
        user = request.user
        if request.method == 'POST':
            otp_entered = request.POST.get('otp_entered')
            base32_secret = request.session.get('base32_secret')
            otp_timestamp = request.session.get('otp_timestamp')
            current_time = int(time.time())
        
            # Calculate OTP validity period
            if base32_secret and otp_timestamp is not None:
                otp_validity_period = 300
            
                # Check if the OTP has expired
                if current_time - otp_timestamp > otp_validity_period:
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('register')
    
                # Verify the OTP using TOTP object
                totp = pyotp.TOTP(base32_secret, interval=otp_validity_period)
                if totp.verify(otp_entered):
                    messages.success(request, 'OTP verified successfully.')
                    username = request.session.get('username')
                    email = request.session.get('email')
                    password = request.session.get('password')
                    user = CustomUser.objects.get(username=username)
                    user.email = email
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    # Clear OTP-related data from session after successful verification
                    del request.session['base32_secret']
                    del request.session['otp_timestamp']
                    del request.session['username']
                    del request.session['email']
                    del request.session['password']
                    return redirect('register_complete')
                else:
                    messages.error(request, 'Invalid OTP. Please try again.')
            else:
                messages.error(request, 'OTP verification failed. No OTP found in session.')
        
        template_name = 'auth/email_verification.html'
        context = {'form':form, 'user':user}
        return render (request, template_name, context)

# use this for email test
def send_email_test(request):
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            # send OTP
            otp, base32_secret = generate_otp()
            
            # Store the secret and timestamp in the session
            request.session['base32_secret'] = base32_secret
            request.session['otp_timestamp'] = int(time.time())

            # send email
            subject = "hello buddy"
            message = render_to_string('experiments/email_template_test.html', {'otp': otp})
            recipient_email = form.cleaned_data['email']
            send_mail(subject,
                      message,
                      from_email=settings.EMAIL_HOST_USER,
                      recipient_list = [recipient_email],
                      fail_silently=False,
                      )
            messages.success(request, 'Email send successfully!')
            return redirect('otp_verify')
        else:
            messages.error(request, 'Email send failed!')
    context = {'form':form}
    template_name = 'experiments/send_email_test.html'
    return render(request, template_name, context)

# test otp verify
def otp_verification_test(request):
    form = OTPForm()
    if request.method == 'POST':
        otp_entered = request.POST.get('otp_entered')
        base32_secret = request.session.get('base32_secret')
        otp_timestamp = request.session.get('otp_timestamp')
        current_time = int(time.time())
        
        # Calculate OTP validity period
        if base32_secret and otp_timestamp is not None:
            otp_validity_period = 300
            
            # Check if the OTP has expired
            if current_time - otp_timestamp > otp_validity_period:
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('send_email')
    
            # Verify the OTP using TOTP object
            totp = pyotp.TOTP(base32_secret, interval=otp_validity_period)
            if totp.verify(otp_entered):
                messages.success(request, 'OTP verified successfully.')
                # Clear OTP-related data from session after successful verification
                del request.session['base32_secret']
                del request.session['otp_timestamp']
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
                return redirect('send_email')
        else:
            messages.error(request, 'OTP verification failed. No OTP or timestamp found in session.')
            return redirect('send_email')
    template_name = 'experiments/otp_verification_test.html'
    context = {'form':form}
    return render (request, template_name, context)

def password_reset(request):
    template_name = 'auth/password_reset.html'
    return render(request, template_name)

@login_required(login_url='login')
def profile(request, pk):
    user = get_object_or_404(CustomUser, user_id=pk)
    template_name = 'profile/profile.html'
    context = {'user':user}
    return render(request, template_name, context)

# @login_required(login_url='login')
def workspace(request):
    workspaces = Workspace.objects.all()
    template_name = 'workspace/workspace.html'
    context = {'workspaces':workspaces}
    return render (request, template_name, context)

@login_required(login_url='login')
def task(request):
    tasks = Task.objects.all()
    template_name = 'workspace/'
    context = {'tasks':tasks}
    return render (request, template_name, context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')