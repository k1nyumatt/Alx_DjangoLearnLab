"""
Unit tests for Book API endpoints

Tests cover:
- CRUD operations
- Filtering, searching, and ordering
- Permissions and authentication
- Response data integrity
- Status codes
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints
    """

    def setUp(self):
        """
        Set up test data and authentication
        
        Creates:
        - Test user with authentication token
        - Sample books for testing
        - API client for making requests
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create authentication token for the user
        self.token = Token.objects.create(user=self.user)
        
        # Create API client
        self.client = APIClient()
        
        # Create sample books for testing
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            author='William S. Vincent',
            publication_year=2021
        )
        
        self.book2 = Book.objects.create(
            title='Python Crash Course',
            author='Eric Matthes',
            publication_year=2019
        )
        
        self.book3 = Book.objects.create(
            title='Django for APIs',
            author='William S. Vincent',
            publication_year=2022
        )
        
        # Define URLs
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')

    def tearDown(self):
        """
        Clean up after each test
        """
        Book.objects.all().delete()
        User.objects.all().delete()
        Token.objects.all().delete()


class BookListViewTests(BookAPITestCase):
    """
    Tests for BookListView (GET /api/books/)
    """

    def test_list_books_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve the book list
        """
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return all 3 books

    def test_list_books_authenticated(self):
        """
        Test that authenticated users can retrieve the book list
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_books_by_title(self):
        """
        Test filtering books by exact title
        """
        response = self.client.get(self.list_url, {'title': 'Django for Beginners'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_filter_books_by_author(self):
        """
        Test filtering books by author
        """
        response = self.client.get(self.list_url, {'author': 'William S. Vincent'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books by this author

    def test_filter_books_by_publication_year(self):
        """
        Test filtering books by publication year
        """
        response = self.client.get(self.list_url, {'publication_year': 2022})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['publication_year'], 2022)

    def test_search_books(self):
        """
        Test searching books by title or author
        """
        response = self.client.get(self.list_url, {'search': 'Django'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should return 2 books with "Django" in title

    def test_search_books_by_author(self):
        """
        Test searching books by author name
        """
        response = self.client.get(self.list_url, {'search': 'Eric'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Eric Matthes')

    def test_order_books_by_title_ascending(self):
        """
        Test ordering books by title (A-Z)
        """
        response = self.client.get(self.list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_title_descending(self):
        """
        Test ordering books by title (Z-A)
        """
        response = self.client.get(self.list_url, {'ordering': '-title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_order_books_by_publication_year(self):
        """
        Test ordering books by publication year
        """
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))

    def test_combined_filter_and_ordering(self):
        """
        Test combining filtering and ordering
        """
        response = self.client.get(
            self.list_url, 
            {'author': 'William S. Vincent', 'ordering': '-publication_year'}
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # First book should be the newer one (2022)
        self.assertEqual(response.data[0]['publication_year'], 2022)


class BookDetailViewTests(BookAPITestCase):
    """
    Tests for BookDetailView (GET /api/books/<id>/)
    """

    def test_retrieve_book_unauthenticated(self):
        """
        Test that unauthenticated users can retrieve a single book
        """
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')
        self.assertEqual(response.data['author'], 'William S. Vincent')

    def test_retrieve_book_authenticated(self):
        """
        Test that authenticated users can retrieve a single book
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.book1.pk)

    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist returns 404
        """
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookCreateViewTests(BookAPITestCase):
    """
    Tests for BookCreateView (POST /api/books/create/)
    """

    def test_create_book_authenticated(self):
        """
        Test that authenticated users can create a new book
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # 3 initial + 1 new
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['author'], 'Test Author')

    def test_create_book_unauthenticated(self):
        """
        Test that unauthenticated users cannot create a book
        """
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 2023
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)  # Should still be 3

    def test_create_book_with_invalid_data(self):
        """
        Test creating a book with invalid data
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # Missing required field 'title'
        data = {
            'author': 'Test Author',
            'publication_year': 2023
        }
        
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_with_invalid_year(self):
        """
        Test creating a book wit