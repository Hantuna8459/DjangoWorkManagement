# Generated by Django 5.0.6 on 2024-07-01 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_customuser_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('TD', 'to do'), ('DOING', 'doing'), ('DONE', 'completed')], default='to do', max_length=10),
        ),
    ]