from django.urls import path
from workspaces import views

urlpatterns = [
    path('workspace_list/', views.workspace_list, name='workspace_list'),
    path('workspace_list/workspace_create/', views.workspace_create, name='workspace_create'),
    path('workspace_list/<uuid:pk>/workspace_update/', views.workspace_update, name='workspace_update'),
    path('workspace_list/<uuid:pk>/workspace_delete/',views.workspace_delete,name='workspace_delete'),
]
