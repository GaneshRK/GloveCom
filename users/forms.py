from django import forms
from django.contrib.auth.models import User
from .models import Profile
import re
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','email')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@gmail\.com$', email):
            raise forms.ValidationError("Please enter a valid Gmail address.")
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email')
        widgets = {
            'email': forms.EmailInput(attrs={
                'readonly': True,    # user cannot type
                'class': 'form-control-plaintext',
    'style':    'color: #bbb;',
            }),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar')
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'id': 'avatar-input',
                'style': 'display:none;'
            }),
        }
