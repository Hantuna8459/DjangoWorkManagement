from django.urls import path
from workspaces import views

urlpatterns = [
    path('workspace_list/', views.workspace_list, name='workspace_list'),
    path('workspace_create/', views.workspace_create, name='workspace_create'),
    path('workspace_list/workspace_delete/<uuid:pk>',views.workspace_delete,name='workspace_delete'),
]
