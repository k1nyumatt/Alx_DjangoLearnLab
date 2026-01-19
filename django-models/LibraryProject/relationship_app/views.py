from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that retrieves all books from the database
    and renders them in a template.
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details of a specific library,
    including all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Registration view
def register(request):
    """
    Handles user registration.
    Creates a new user account and logs them in automatically.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('list_books')  # Redirect to books list after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test

# Helper functions to check user roles
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view - only accessible by Admin users
@user_passes_test(is_admin)
def admin_view(request):
    """
    View accessible only to users with Admin role.
    """
    return render(request, 'relationship_app/admin_view.html')


# Librarian view - only accessible by Librarian users
@user_passes_test(is_librarian)
def librarian_view(request):
    """
    View accessible only to users with Librarian role.
    """
    return render(request, 'relationship_app/librarian_view.html')


# Member view - only accessible by Member users
@user_passes_test(is_member)
def member_view(request):
    """
    View accessible only to users with Member role.
    """
    return render(request, 'relationship_app/member_view.html')