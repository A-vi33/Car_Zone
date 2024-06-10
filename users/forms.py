from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Order

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Remove help texts
        for field_name, field in self.fields.items():
            field.help_text = ""

        # Set required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        # Add placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Your Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Your Password'})
        

class UserUpdateForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Remove help texts
        for field_name, field in self.fields.items():
            field.help_text = ""

        # Set required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        # Add placeholders
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        
        