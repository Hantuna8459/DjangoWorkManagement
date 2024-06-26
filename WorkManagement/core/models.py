from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUser(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, null=False)
    phone_number = models.CharField(max_length=10)
    user_image = models.ImageField(upload_to='profile_images', default='profile_images/blank-profile-picture.png')
    
    class Meta:
        db_table = 'user'
    
class Workspace(models.Model):
    workspace_id = models.BigAutoField(primary_key=True, null=False)
    workspace_label = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'workspace'
    
    def __str__(self):
        return self.workspace_label

class Task(models.Model):
    task_id = models.IntegerField(primary_key=True, null=False)
    task_label = models.CharField(max_length=50)
    task_status = models.CharField(max_length=20)
    task_description = models.CharField(max_length=255)
    task_image = models.ImageField(upload_to='task_images', default=None)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'task'
    
    def __str__(self):
        return self.task_label