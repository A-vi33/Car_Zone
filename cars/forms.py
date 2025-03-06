from django import forms

from cars.models import Comment
from users.models import Order
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('car',)
    
        widgets = {
                'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
                'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
                'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your Comment'})
            }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'