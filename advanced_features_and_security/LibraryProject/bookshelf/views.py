from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm, ExampleForm


# View to list all books with search functionality (requires can_view permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books with optional search functionality.
    Requires: can_view permission
    
    Security measures:
    - Uses Django ORM to prevent SQL injection
    - Validates and sanitizes user input through ORM queries
    """
    books = Book.objects.all()
    
    # Secure search functionality using Django ORM (prevents SQL injection)
    search_query = request.GET.get('search', '')
    if search_query:
        # Using Django ORM's Q objects for safe querying - prevents SQL injection
        # Never use raw SQL or string formatting for user input
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


# View to create a new book (requires can_create permission)
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Create a new book.
    Requires: can_create permission
    
    Security measures:
    - CSRF token protection (handled by Django middleware and template)
    - Input validation through Django ORM
    - Safe parameter handling
    """
    if request.method == 'POST':
        # Safely retrieve and validate user input
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        publication_year = request.POST.get('publication_year', '').strip()
        
        # Basic validation
        if title and author:
            # Use Django ORM create method - prevents SQL injection
            # Never use raw SQL or string interpolation
            try:
                year = int(publication_year) if publication_year else None
                Book.objects.create(
                    title=title,
                    author=author,
                    publication_year=year
                )
                messages.success(request, 'Book created successfully!')
                return redirect('book_list')
            except ValueError:
                messages.error(request, 'Invalid publication year.')
        else:
            messages.error(request, 'Title and author are required.')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})


# View to edit an existing book (requires can_edit permission)
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Edit an existing book.
    Requires: can_edit permission
    
    Security measures:
    - Uses get_object_or_404 to safely retrieve objects
    - CSRF token protection
    - Input validation
    """
    # Safely retrieve book using ORM - prevents SQL injection
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        publication_year = request.POST.get('publication_year', '').strip()
        
        if title and author:
            try:
                # Update using ORM - safe from SQL injection
                book.title = title
                book.author = author
                book.publication_year = int(publication_year) if publication_year else None
                book.save()
                messages.success(request, 'Book updated successfully!')
                return redirect('book_list')
            except ValueError:
                messages.error(request, 'Invalid publication year.')
        else:
            messages.error(request, 'Title and author are required.')
    
    return render(request, 'bookshelf/book_form.html', {
        'book': book,
        'action': 'Edit'
    })


# View to delete a book (requires can_delete permission)
@permission_required('bookshelf.can_delete', raise_exception=True)
def book