from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # List all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Get single book details
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update existing book (matching test requirements)
    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete book (matching test requirements)
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
]
]