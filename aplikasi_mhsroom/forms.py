from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'photo']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']