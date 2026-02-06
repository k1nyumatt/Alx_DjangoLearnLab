"""
Unit tests for Book API endpoints

Tests cover:
- CRUD operations
- Filtering, searching, and ordering
- Permissions and authentication (Token and Session)
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
        self.assertEqual(len(response.data), 3)

    def test_list_books_authenticated(self):
        """
        Test that authenticated users can retrieve the book list
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_list_books_with_login(self):
        """
        Test that logged-in users can retrieve the book list
        """
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.client.logout()

    def test_filter_books_by_title(self):
        """
        Test filtering books by exact title
        """
        response = self.cli