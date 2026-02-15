from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    Includes tagging functionality.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add tags separated by commas (e.g., python, django, web)',
                'data-role': 'tagsinput'
            })
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
            'tags': 'Tags'
        }
        help_texts = {
            'title': 'Enter a descriptive title for your post',
            'content': 'Write the main content of your blog post',
            'tags': 'Separate tags with commas. New tags will be created automatically.'
        }


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments on blog posts.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4
            })
        }
        labels = {
            'content': 'Your Comment'
        }
        help_texts = {
            'content': 'Share your thoughts about this post'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError('Comment cannot be empty.')
        return content