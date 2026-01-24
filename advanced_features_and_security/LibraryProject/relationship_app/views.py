from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Book, Library, Author
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required


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

# View to add a new book - requires 'can_add_book' permission
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View to add a new book.
    Only accessible to users with 'can_add_book' permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            author = Author.objects.get(id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


# View to edit an existing book - requires 'can_change_book' permission
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View to edit an existing book.
    Only accessible to users with 'can_change_book' permission.
    """
    book = Book.objects.get(id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author')
        book.author = Author.objects.get(id=author_id)
        book.save()
        return redirect('list_books')
    
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


# View to delete a book - requires 'can_delete_book' permission
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View to delete a book.
    Only accessible to users with 'can_delete_book' permission.
    """
    book = Book.objects.get(id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book

# View to list all books (requires can_view permission)
@permission_required('relationship_app.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books.
    Requires: can_view permission
    """
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})


# View to create a new book (requires can_create permission)
@permission_required('relationship_app.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    Requires: can_create permission
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
    
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/book_form.html', {'authors': authors, 'action': 'Create'})


# View to edit an existing book (requires can_edit permission)
@permission_required('relationship_app.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    Requires: can_edit permission
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/book_form.html', {
        'book': book,
        'authors': authors,
        'action': 'Edit'
    })


# View to delete a book (requires can_delete permission)
@permission_required('relationship_app.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Delete a book.
    Requires: can_delete permission
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})