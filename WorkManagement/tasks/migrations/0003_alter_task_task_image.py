# Generated by Django 5.0.6 on 2024-07-08 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='task_images'),
        ),
    ]
