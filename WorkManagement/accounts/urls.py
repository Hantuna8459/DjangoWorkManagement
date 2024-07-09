from django.urls import path
from django.views.generic import TemplateView
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('pasword_change/', views.change_password_view, name ='password_change'),
    path('password_set/', views.set_password_view, name='password_set'),
    path('register/', views.register_view, name='register'),
    path('agreement',TemplateView.as_view(template_name='terms_and_conditions.html'), name='agreement'),
    path('logout/', views.logout_view, name='logout'),
    path('register/email_verification/', views.email_verify_view, name='email_verification'),
    path('register/email_verification/register_complete', TemplateView.as_view(template_name='workspaces/register_complete.html'), name = 'register_complete'),
    path('profile_update/<uuid:pk>/', views.profile_update_view, name='profile_update'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
