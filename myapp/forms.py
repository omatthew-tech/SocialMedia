from django import forms
from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'twitter_link', 'instagram_link', 'personal_website')

