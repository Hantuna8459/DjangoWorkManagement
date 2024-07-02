from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    phone_number = models.CharField(max_length=10)
    user_image = models.ImageField(upload_to='profile_images', default='profile_images/blank-profile-picture.png')
    
    class Meta:
        db_table = 'user'