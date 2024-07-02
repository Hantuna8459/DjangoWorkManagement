from django.urls import path
from django.views.generic import TemplateView
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('login/password_reset/password_reset_complete', auth_views.PasswordResetDoneView.as_view(template_name = '') ,name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('agreement',TemplateView.as_view(template_name='terms_and_conditions.html'), name='agreement'),
    path('logout/', views.logout_view, name='logout'),
    path('register/email_verification', views.email_verify, name='email_verification'),
    path('register/email_verification/register_complete', TemplateView.as_view(template_name='auth/register_complete.html'), name = 'register_complete'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    # experiments
    path('send_email', views.send_email_test, name='send_email'),
    path('send_email/otp_verify', views.otp_verification_test, name='otp_verify')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
