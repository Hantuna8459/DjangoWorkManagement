from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import(
    CustomRegisterForm, 
    CustomLoginForm,
    EmailVerifyForm,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import CustomUser
import pyotp
import time
from django.http import HttpResponse, JsonResponse
from accounts.utils import generate_otp

# Create your views here.

def login_view(request):
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
                        return redirect('workspace_list')
                    else:
                        request.session.set_expiry(0)
                    return redirect('workspace_list')
    else:
        form = CustomLoginForm() 
    template_name = 'auth/login.html'
    context = {'form':form}
    return render(request, template_name, context)

def register(request):
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
    else:
        form = EmailVerifyForm()
        template_name = 'auth/email_verification.html'
        context = {'form':form, 'user':user}
        return render (request, template_name, context)

def password_reset(request):
    template_name = 'auth/password_reset.html'
    return render(request, template_name)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request, pk):
    user = get_object_or_404(CustomUser, user_id=pk)
    template_name = 'profile/profile.html'
    context = {'user':user}
    return render(request, template_name, context)