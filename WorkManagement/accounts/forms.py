from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Enter Username or Email'
        
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
    
    login_save = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label='Remember me ?'
    )
    
class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='', 
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Enter your Email Address',
            }
        )
    )    
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        
    def __init__(self, *args, **kwargs):
        super(CustomRegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your Username'
        self.fields['username'].help_text = ''

        self.fields['password1'].label = ''
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password cannot be entirely numeric.</li>'
            '</ul>'
        )
        
        self.fields['password2'].label = ''
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].help_text = (
            '<span class="form-text">'
            '<p>Enter the same password as before</p>'
            '</span>'	
        )
        
class EmailVerifyForm(forms.Form):
    otp_entered = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Enter OTP here',
            })
    )
            
# experiments forms
class EmailForm(forms.Form):
    email = forms.EmailField(
        label='', 
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Enter your Email Address',
            'help_text':'doesnot matter',
            }
        )
    )
        
class OTPForm(forms.Form):
    otp_entered = forms.CharField(
        label='enter OTP',
    )