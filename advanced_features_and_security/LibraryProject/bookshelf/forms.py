from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Django ModelForm for Book model.
    
    Security features:
    - Automatic input validation and sanitization
    - Protection against XSS through Django's form rendering
    - Built-in CSRF protection when used with {% csrf_token %}
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'required': True
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'required': True
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter publication year (optional)'
            }),
        }
    
    def clean_title(self):
        """
        Custom validation for title field.
        Ensures title is not empty and strips whitespace.
        """
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if not title:
                raise forms.ValidationError("Title cannot be empty or only whitespace.")
        return title
    
    def clean_author(self):
        """
        Custom validation for author field.
        Ensures author is not empty and strips whitespace.
        """
        author = self.cleaned_data.get('author')
        if author:
            author = author.strip()
            if not author:
                raise forms.ValidationError("Author cannot be empty or only whitespace.")
        return author
    
    def clean_publication_year(self):
        """
        Custom validation for publication year.
        Ensures the year is reasonable if provided.
        """
        year = self.cleaned_data.get('publication_year')
        if year is not None:
            if year < 0 or year > 9999:
                raise forms.ValidationError("Please enter a valid publication year.")
        return year


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django form security features.
    
    Security benefits:
    - Automatic HTML escaping of input
    - Built-in validation
    - CSRF protection when rendered with {% csrf_token %}
    - XSS protection through safe rendering
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name'
        }),
        help_text='Enter your full name'
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        }),
        help_text='Enter a valid email address'
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message',
            'rows': 4
        })
    )
    
    def clean_name(self):
        """Validate and sanitize name input."""
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            if not name:
                raise forms.ValidationError("Name cannot be empty.")
        return name