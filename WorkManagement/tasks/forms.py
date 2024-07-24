from django import forms
from tasks.models import Task
from django_ckeditor_5.widgets import CKEditor5Widget

# Create your form here

class TaskCreateForm(forms.ModelForm):
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
    
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_label',
            'task_description',
            'task_status',
            'task_image',
        ]
        def __init__(self, *args, **kwargs):
            super(TaskUpdateForm, self).__init__(*args, **kwargs)
            self.fields['task_status'].choices = Task.TASK_STATUS_CHOICES

        