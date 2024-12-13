from django import forms
from .models import Post, Comment
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title", 'content']
        widgets = {
            'title': forms.widgets.TextInput(attrs={'class': 'input', 'id':'title'}),
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30, 'class':'input','id':'content'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']