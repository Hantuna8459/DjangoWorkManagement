from django.contrib import admin
from core.models import (
    CustomUser,
    Workspace,
    Task,
    )

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Workspace)
admin.site.register(Task)