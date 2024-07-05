from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('task_list/', views.task_list, name='task_list'),
    path('task_create', views.task_create, name='task_create'),
    path('task_update/<uuid:pk>', views.task_update, name='task_update'),
    path('task_delete/<uuid:pk>', views.task_delete, name='task_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
