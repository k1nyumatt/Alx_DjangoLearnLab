"""
Models for the API application.

This module defines the data models for managing authors and books in our API.
The models establish a one-to-many relationship where one author can have multiple books.

Models:
    - Author: Represents book authors
    - Book: Represents books written by authors

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']

Relationships:
    - One Author can have Many Books (One-to-Many)
    - Each Book belongs to exactly One Author
    - This is implemented using Django's ForeignKey field
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing book authors.
    
    This model stores information about authors who write books.
    Each author can be associated with multiple books through a foreign key relationship
    defined in the Book model.
    
    Fields:
        name (CharField): The full name of the author.
                         - max_length=200: Limits the name to 200 characters
                         - This is a required field (blank=False by default)
    
    Relationships:
        books (reverse relationship): Accessed via the 'books' related_name from Book model
                                     - Use author.books.all() to get all books by this author
                                     - This is a reverse ForeignKey relationship
                                     - Returns a QuerySet of Book objects
    
    Methods:
        __str__: Returns the author's name for readable representation in admin and shell
    
    Example:
        # Create an author
        author = Author.objects.create(name="J.K. Rowling")
        
        # Access all books by this author (reverse relationship)
        books = author.books.all()
    """
    
    # CharField stores text data with a maximum length
    # This field is required by default (blank=False, null=False)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        """
        String representation of the Author.
        
        Returns:
            str: The author's name
        """
        return self.name
    
    class Meta:
        # Optional: Add ordering, verbose names, etc.
        ordering = ['name']  # Orders authors alphabetically by name
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    """
    Book model representing books written by authors.
    
    This model stores information about books and establishes a many-to-one relationship
    with the Author model. Multiple books can be associated with a single author.
    
    Fields:
        title (CharField): The title of the book
                          - max_length=200: Limits title to 200 characters
                          - Required field
        
        publication_year (IntegerField): The year the book was published
                                        - Stores as integer (e.g., 2005, 1997)
                                        - Validated in serializer to prevent future dates
        
        author (ForeignKey): Foreign key linking to the Author model
                           - Establishes the many-to-one relationship
                           - on_delete=models.CASCADE: If author is deleted, all their books are deleted
                           - related_name='books': Allows reverse access from Author to Books
                           
    Relationships:
        author (ForeignKey): Many-to-one relationship with Author
                            - Many Books can belong to One Author
                            - Required field (every book must have an author)
                            - Creates author_id column in database
                            - Access author from book: book.author
                            - Access books from author: author.books.all()
    
    Methods:
        __str__: Returns the book title and publication year for readable representation
    
    Example:
        # Create a book linked to an author
        author = Author.objects.get(name="J.K. Rowling")
        book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=author
        )
        
        # Access the author from a book
        print(book.author.name)  # "J.K. Rowling"
        
        # Access all books by an author (reverse relationship)
        all_books = author.books.all()
    """
    
    # CharField for book title - stores text up to 200 characters
    title = models.CharField(max_length=200)
    
    # IntegerField for publication year - stores integer values
    # No max/min constraints at model level - validation happens in serializer
    publication_year = models.IntegerField()
    
    # ForeignKey creates the one-to-many relationship between Author and Book
    # Parameters explained:
    # - Author: The model this field references
    # - on_delete=models.CASCADE: Delete books when author is deleted
    # - related_name='books': Reverse relation name (author.books.all())
    author = models.ForeignKey(
        Author,                    # Reference to Author model
        on_delete=models.CASCADE,  # Cascade deletion
        related_name='books'       # Reverse relation accessor
    )
    
    def __str__(self):
        """
        String representation of the Book.
        
        Returns:
            str: Book title and publication year in format "Title (Year)"
        """
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        # Optional: Add ordering, indexes, etc.
        ordering = ['-publication_year', 'title']  # Newest books first
        verbose_name = 'Book'
        verbose_name_plural = 'Books'