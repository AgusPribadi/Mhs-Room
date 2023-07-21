from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, Comment

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'photo']  # Add 'user' and 'photo' fields for editing

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    
    tagged_users = forms.CharField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Comment
        fields = ['content', 'tagged_users']

    def save(self, commit=True):
        instance = super().save(commit=False)
        mentions = instance.get_mentions()

        if commit:
            instance.save()

        return instance, mentions