from django import forms
from tasks.models import Task
from ckeditor.widgets import CKEditorWidget

# Create your form here

class TaskCreateForm(forms.ModelForm):
    task_description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Task
        fields = [
            'task_label',
            'task_status',
            'task_description',
            'task_images',
        ]
    
    field_order = [
        'task_label',
        'task_description',
        'task_images',
        'task_status',
        ]  
        