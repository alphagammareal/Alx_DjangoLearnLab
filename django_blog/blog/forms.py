from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from taggit.forms import TagWidget  # make sure this line exists

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'class': 'tag-input'}),  # TagWidget() must appear here
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)
