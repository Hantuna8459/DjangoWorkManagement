from django import forms
from workspaces.models import Workspace

class WorkspaceCreateForm(forms.ModelForm):
    workspace_label = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Enter workspace title here',
            })
    )
    
    class Meta:
        model = Workspace
        fields = ['workspace_label']
        
class WorkspaceUpdateForm(WorkspaceCreateForm):
    pass