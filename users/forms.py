from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.CharField(
        required=True,
        widget =  forms.EmailInput(attrs={'placeholder': 'Email Address'}),
    )
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            # 'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
    password1 = forms.CharField(
    label="Password",
    widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )