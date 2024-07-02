from django.db import models
import uuid
from accounts.models import CustomUser

# Create your models here.

class Workspace(models.Model):
    workspace_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    workspace_label = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'workspace'
    
    def __str__(self):
        return self.workspace_label