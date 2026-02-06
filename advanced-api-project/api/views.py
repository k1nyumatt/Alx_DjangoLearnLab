"""
API Views for Book model using Django REST Framework Generic Views
"""

from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


# ListView - Retrieve all books
class BookListView(generics.ListAPIView):
    """
    GET: Returns a list of all books
    Accessible to all users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# DetailView - Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Returns details of a specific book by ID
    Accessible to all users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# CreateView - Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Creates a new book instance
    Only accessible to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """Custom logic during book creation"""
        serializer.save()


# UpdateView - Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Updates an existing book
    Only accessible to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        """Custom logic during book update"""
        serializer.save()


# DeleteView - Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Removes a book instance
    Only accessible to authenticated users
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
