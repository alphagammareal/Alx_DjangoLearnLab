from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagField


class PostForm(forms.ModelForm):
    tags = TagField(required=False)  # use TagField for tags

    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'published_date', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
