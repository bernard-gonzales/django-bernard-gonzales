from django import forms
from .models import Comment

class PostForm(forms.ModelForm):
        class Meta:
                model = Comment
                fields = {'title', 'comment_text'}

                widgets = {
                        'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type Title Here'}),
                        'comment_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type Comment Here'}),
                }