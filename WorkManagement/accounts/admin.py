from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.

@admin.action(description="deactivate account")
def deactivate_account(modeladmin, request, queryset):
    queryset.update(is_active=False)
    
admin.site.register(CustomUser)

