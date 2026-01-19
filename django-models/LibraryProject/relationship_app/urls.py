from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view for listing books
    path('books/', list_books, name='list_books'),
    
    # Class-based view for library detail
    # <int:pk> captures the library ID from the URL
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]