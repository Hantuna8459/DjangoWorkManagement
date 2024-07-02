from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('task_list/<uuid:pk>/', views.task_list, name = 'task_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
