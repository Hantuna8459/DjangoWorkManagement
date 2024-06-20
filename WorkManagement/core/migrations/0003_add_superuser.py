from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations

def generate_superuser(apps, schema_editor):
    User = apps.get_model("core.CustomUser") 
    username = settings.DJANGO_SUPERUSER_NAME
    email = settings.DJANGO_SUPERUSER_EMAIL
    password = settings.DJANGO_SUPERUSER_PASSWORD

    if not User.objects.filter(email=email).exists():
        user = User()
        user.email = email
        user.username = username
        user.password = make_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customuser_is_staff'),
    ]

    operations = [
        migrations.RunPython(generate_superuser),
    ]
