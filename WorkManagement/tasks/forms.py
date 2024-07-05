from django import forms
from tasks.models import Task

# Create your form here

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'