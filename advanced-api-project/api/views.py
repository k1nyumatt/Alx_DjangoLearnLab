"""
API Views for Book model using Django REST Framework Generic Views
with Filtering, Searching, and Ordering capabilities
"""

from rest_framework import generics, permissions, filters
from django_filters import rest_framework
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListView - Retrieve all books with filtering, searching, and ordering
    
    HTTP Method: GET
    Endpoint: /api/books/
    Permission: Anyone (authenticated or not)
    
    Query Parameters:
    - Filtering:
      * ?title=<value>              - Filter by exact title
      * ?author=<value>             - Filter by exact author name
      * ?publication_year=<value>   - Filter by exact publication year
    
    - Searching:
      * ?search=<value>             - Search in title and author fields
    
    - Ordering:
      * ?ordering=title             - Order by title (A-Z)
      * ?ordering=-title            - Order by title (Z-A)
      * ?ordering=publication_year  - Order by year (oldest first)
      * ?ordering=-publication_year - Order by year (newest first)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Enable filtering, searching, and ordering
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering: Specify which fields can be filtered
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Searching: Specify which fields can be searched
    search_fields = ['title', 'author']
    
    # Ordering: Specify which fields can be used for ordering
    ordering_fields = ['title', 'author', 'publication_year']
    
    # Default ordering (optional)
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView - Retrieve a single book by ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView - Add a new book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        """Custom logic during book creation"""
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView - Modify an existing book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_update(self, serializer):
        """Custom logic during book update"""
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView - Remove a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]