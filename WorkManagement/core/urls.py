from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/password_reset/', views.password_reset, name='password_reset'),
    path('register/', views.register, name='register'),
    path('agreement',TemplateView.as_view(template_name='terms_and_conditions.html'), name='agreement'),
    path('workspace/', views.workspace, name='workspace'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('register/email_verification', views.email_verify, name='email_verification'),
    path('register/email_verification/register_complete', TemplateView.as_view(template_name='auth/register_complete.html'), name = 'register_complete'),
    path('profile', views.profile, name='profile'),
    # experiments
    path('send_email', views.send_email_test, name='send_email'),
    path('send_email/otp_verify', views.otp_verification_test, name='otp_verify')
]
