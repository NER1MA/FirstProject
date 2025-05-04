from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'style': 'resize: vertical; font-size:14px; padding:8px;'
            }),
            'author': forms.TextInput(attrs={
                'style': 'font-size:14px; padding:6px;'
            }),
        }