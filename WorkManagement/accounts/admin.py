from django.contrib import admin
from accounts.models import CustomUser

# Register your models here.

# @admin.action(description="deactivate account")
# def deactivate_account(modeladmin, request):
#     CustomUser.is_active

admin.site.register(CustomUser)

