from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Workspace(models.Model):
    workspace_id = models.BigAutoField(primary_key=True, null=False)
    workspace_label = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'workspace'
    
    def __str__(self):
        return self.workspace_label