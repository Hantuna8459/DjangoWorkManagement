from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUser(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, null=False)
    phone_number = models.CharField(max_length=10)
    user_image = models.ImageField(upload_to='profile_images', default='profile_images/blank-profile-picture.png')
    
    class Meta:
        db_table = 'user'