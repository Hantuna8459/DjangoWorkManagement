from django import forms
from .models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
    
)

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
        
    field_order = ["email","username","password1","password2"]
        
class EmailVerifyForm(forms.Form):
    
    otp_entered = forms.IntegerField(
        label='',
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Enter OTP here',
            }),
    )
    
class CustomPasswordReset(PasswordResetForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomPasswordReset, self).__init__(*args, **kwargs)
        
        self.fields['email'].label = ''
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'
        self.fields['email'].help_text = (
            '<span>Please enter your email so we can reset your password</span>'
        )
        
class CustomSetPassword(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPassword, self).__init__(*args, **kwargs)
        
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter your Email'
        self.fields['new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password cannot be entirely numeric.</li>'
            '</ul>'
        )
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].help_text = (
            '<span class="form-text">'
            '<p>Enter the same password as before</p>'
            '</span>'	
        )
        
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomSetPassword, self).__init__(*args, **kwargs)
        
        self.fields['old_password'].label = ''
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter your old Password'
        self.fields['old_password'].help_text = (
            '<span></span>'
        )
        
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter your Email'
        self.fields['new_password1'].help_text = (
            '<ul class="form-text text-muted small">'
            '<li>Your password must contain at least 8 characters.</li>'
            '<li>Your password cannot be entirely numeric.</li>'
            '</ul>'
        )
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].help_text = (
            '<span class="form-text">'
            '<p>Enter the same password as before</p>'
            '</span>'	
        )
        
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
        'user_image',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        ]
        
    phone_number = forms.CharField(
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'type': 'range',
            'min': '0100000001',
            'max': '0999999999',
            'step': '1',
            'value': '0100000001',
            'class': 'form-range'
        }),
        help_text='<p>Your phone number is: <span id="value"</p>',
    )
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your Username'
        self.fields['username'].help_text = ''
        
        self.fields['first_name'].label = ''
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your First Name'
        self.fields['first_name'].help_text = ''
        
        self.fields['last_name'].label = ''
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your Last Name'
        self.fields['last_name'].help_text = ''