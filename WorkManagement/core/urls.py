from django.urls import path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('register/', views.register_view, name='register'),
    path('agreement',TemplateView.as_view(template_name='terms_and_conditions.html'), name='agreement'),
    path('workspace/', views.workspace_view, name='workspace'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'),name='logout'),
]
