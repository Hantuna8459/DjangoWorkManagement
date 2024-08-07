from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import(
    CustomRegisterForm, 
    CustomLoginForm,
    EmailVerifyForm,
    ProfileForm,
    CustomSetPassword,
    CustomPasswordChangeForm,
    CustomPasswordReset,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import CustomUser
import pyotp
import time
from accounts.utils import generate_otp
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']     
            user = authenticate(request, username=username, password=password)
            login_save = request.POST.get('login_save')
            if user is not None:
                if user.is_active == True:
                    request.session.set_expiry(login_save and 172800 or 0)
                    login(request, user)
                    return redirect('workspace_list')
                else:
                    messages.error(request, 'This account is deactivated, please contact admin')
            else:
                messages.error(request, 'User Unavailable')
    else:
        form = CustomLoginForm() 
    template_name = 'accounts/login.html'
    context = {'form':form}
    return render(request, template_name, context)

def register_view(request):
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
            subject = "Your Account Registration"
            message = render_to_string('accounts/register_email.html', {
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
    template_name = 'accounts/register.html'
    context = {'form':form}
    return render (request, template_name, context)

def email_verify_view(request):
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
        template_name = 'accounts/email_verification.html'
        context = {'form':form, 'user':user}
        return render (request, template_name, context)

def password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordReset(request.POST)
        if form.is_valid():
            current_site = get_current_site(request)
            user = request.user
            
            # Send Email
            subject = "Password Reset"
            message = render_to_string('accounts/password_reset_email.html',{
                'user':user,
                'domain': current_site.domain,
            })
            recipient_email = form.cleaned_data['email']
            send_mail(
                subject,
                message,
                from_email=('noreply@mail.com'),
                recipient_list = [recipient_email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = CustomPasswordReset() 
    template_name = 'accounts/password_reset.html'
    context = {'form':form}
    return render(request, template_name, context)

def set_password_view(request):
    if request.method == 'POST':
        form = CustomSetPassword(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSetPassword(user=request.user)
    template = 'accounts/password_set.html'
    context = {'form':form}
    return render(request, template, context)

def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile_update')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    template = 'accounts/'
    context = {'form':form}
    return render(request, template, context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

@login_required(login_url='login')
def profile_update_view(request, pk):
    user = get_object_or_404(CustomUser, user_id=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update User successfully!')
    else:
        form = ProfileForm(instance=user)        
    template_name = 'accounts/profile_update.html'
    context = {'form':form}
    return render(request, template_name, context)