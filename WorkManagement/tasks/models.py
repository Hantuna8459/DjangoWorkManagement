from django.db import models
import uuid
from workspaces.models import Workspace

# Create your models here.

class Task(models.Model):
    
    TASK_STATUS_CHOICES = {
        "TD":"to do",
        "DG":"doing",
        "DN":"done",
    }
    
    task_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    task_label = models.CharField(max_length=50)
    task_status = models.CharField(max_length=2, choices=TASK_STATUS_CHOICES, default="TD")
    task_description = models.CharField(max_length=255)
    task_image = models.ImageField(upload_to='task_images', default=None)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'task'
    
    def __str__(self):
        return self.task_label
