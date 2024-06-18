from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import(
    CustomRegisterForm, 
    CustomLoginForm,
    EmailForm,
    OTPForm,
)
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
import time
import pyotp

# Create your views here.

def login_view(request):
    form = CustomLoginForm()
    if request.method == 'POST':
        form = CustomLoginForm(data = request.POST)
        username_or_email = request.POST.get('username') or request.POST.get('email')
        password = request.POST.get('password')       
        user = authenticate(request, username=username_or_email, password=password)
        login_save = request.POST.get('login_save')# manual set cookie expire age
        if user is not None:
            login(request, user)
            if login_save:
                request.session.set.expiry(1000000)
            else:
                request.session.set.expiry(0)
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

def generate_otp():
    base32_secret = pyotp.random_base32()
    totp = pyotp.TOTP(base32_secret)
    otp = totp.now()
    return otp, base32_secret

# use this for email test
def send_email_test(request):
    form = EmailForm()
    if request.method == 'POST':
        form = EmailForm(data=request.POST)
        if form.is_valid():
            
            # Generate OTP
            base32_secret = pyotp.random_base32()
            totp = pyotp.TOTP(base32_secret)
            otp = totp.now()
            
            # Store the secret and OTP in session for later verification
            request.session['base32_secret'] = base32_secret
            request.session['otp'] = otp
            
            # send email
            subject = "hello buddy"
            message = render_to_string('email_template_test.html', {'otp': otp})
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
    template_name = 'send_email_test.html'
    return render(request, template_name, context)

# test otp verify
def otp_verification_test(request):
    form = OTPForm()
    if request.method == 'POST':
        otp_entered = request.POST.get('otp_entered')
        base32_secret = request.session.get('base32_secret')
        otp_timestamp = request.session.get('otp_timestamp')
        current_time = int(time.time())
    
        # Calculate OTP validity period (e.g., 300 seconds)
        otp_validity_period = 300

        if current_time - otp_timestamp > otp_validity_period:
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('send_email_test')
    
    
        # Verify the OTP using TOTP object
        totp = pyotp.TOTP(base32_secret, interval=otp_validity_period)
        if totp.verify(otp_entered):
            messages.success(request, 'OTP verified successfully.')
            # Clear OTP-related data from session after successful verification
            del request.session['otp']
            del request.session['base32_secret']
            del request.session['otp_timestamp']
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    template_name = 'otp_verification_test.html'
    context = {'form':form}
    return render (request, template_name, context)

def password_reset_view(request):
    template_name = 'auth/password_reset.html'
    return render(request, template_name)

@login_required(login_url='login')
def workspace_view(request):
    template_name = 'workspace/workspace.html'
    return render (request, template_name)
