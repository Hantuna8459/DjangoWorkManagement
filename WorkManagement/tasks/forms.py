from django import forms
from tasks.models import Task
from django_ckeditor_5.widgets import CKEditor5Widget

# Create your form here

class TaskCreateForm(forms.ModelForm):
    task_description = forms.CharField(widget="")
    class Meta:
        model = Task
        fields = [
            'task_label',
            'task_description',
            'task_image',
        ]
    
    field_order = [
        'task_label',
        'task_description',
        'task_image',
        ]
    
class TaskUpdateForm(TaskCreateForm):
    task_status = forms.ChoiceField()
    class Meta:
        field_order = [
            'task_label',
            'task_description',
            'task_status'
            'task_image',
        ]

        