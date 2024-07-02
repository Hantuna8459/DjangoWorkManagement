from django.db import models
from workspaces.models import Workspace

# Create your models here.

class Task(models.Model):
    TODO = "TD"
    DOING = "DOING"
    DONE = "DONE"
    
    TASK_STATUS_CHOICES = {
        TODO:"to do",
        DOING:"doing",
        DONE:"completed",
    }
    
    task_id = models.IntegerField(primary_key=True, null=False)
    task_label = models.CharField(max_length=50)
    task_status = models.CharField(max_length=10, choices=TASK_STATUS_CHOICES, default="to do")
    task_description = models.CharField(max_length=255)
    task_image = models.ImageField(upload_to='task_images', default=None)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'task'
    
    def __str__(self):
        return self.task_label
