"""
Serializers for the API application.

This module defines serializers for converting Author and Book model instances
to/from JSON format for the REST API. It includes nested serialization and 
custom validation.

Serializers:
    - BookSerializer: Handles Book model serialization with validation
    - AuthorSerializer: Handles Author model with nested Book serialization

Key Concepts:
    - Serialization: Converting Django model instances to JSON
    - Deserialization: Converting JSON to Django model instances
    - Nested Serialization: Including related objects in the response
    - Custom Validation: Adding business logic validation rules

Relationship Handling:
    The relationship between Author and Book is handled using NESTED SERIALIZATION.
    
    How it works:
    1. BookSerializer serializes individual Book instances
    2. AuthorSerializer includes a 'books' field that uses BookSerializer
    3. The 'books' field is set to many=True (one author, many books)
    4. The 'books' field uses the related_name='books' from the Book.author ForeignKey
    5. When an Author is serialized, all related Books are automatically included
    
    Example JSON output:
    {
        "id": 1,
        "name": "J.K. Rowling",
        "books": [
            {
                "id": 1,
                "title": "Harry Potter and the Philosopher's Stone",
                "publication_year": 1997,
                "author": 1
            },
            {
                "id": 2,
                "title": "Harry Potter and the Chamber of Secrets",
                "publication_year": 1998,
                "author": 1
            }
        ]
    }
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer converts Book model instances to/from JSON format.
    It includes all fields from the Book model and adds custom validation
    for the publication_year field.
    
    Purpose:
        - Serialize Book objects to JSON for API responses
        - Deserialize JSON to Book objects for creating/updating books
        - Validate book data before saving to database
    
    Fields:
        id (int): Auto-generated primary key (read-only)
        title (str): Book title (required, max 200 chars)
        publication_year (int): Year of publication (required, validated)
        author (int): Foreign key ID referencing Author (required)
    
    Validation:
        - title: Automatically validated by max_length from model
        - publication_year: Custom validation to prevent future dates
        - author: Must reference an existing Author ID
    
    Usage Example:
        # Serialize a book instance
        book = Book.objects.get(id=1)
        serializer = BookSerializer(book)
        json_data = serializer.data
        
        # Deserialize JSON to create a book
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": 1
        }
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
    """
    
    class Meta:
        model = Book
        # Include all fields in serialization
        fields = ['id', 'title', 'publication_year', 'author']
        # Alternative: fields = '__all__'  # Would include all fields automatically
    
    def validate_publication_year(self, value):
        """
        Custom validation method for the publication_year field.
        
        This method is automatically called during deserialization when
        validating the publication_year field. It ensures that books cannot
        have a publication year in the future.
        
        Validation Rules:
            - publication_year must be <= current year
            - If validation fails, raises ValidationError
            - If validation passes, returns the value
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year if valid
            
        Raises:
            serializers.ValidationError: If publication year is in the future
        
        Example:
            # This will pass validation
            data = {"publication_year": 2023}
            
            # This will fail validation (assuming current year is 2024)
            data = {"publication_year": 2025}
            # Raises: ValidationError("Publication year cannot be in the future...")
        """
        current_year = datetime.now().year
        
        # Check if the publication year is in the future
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        # Return the value if validation passes
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with NESTED Book serialization.
    
    This serializer demonstrates NESTED SERIALIZATION by including related
    Book instances within the Author serialization. When an Author is serialized,
    all of their books are automatically included in the response.
    
    Purpose:
        - Serialize Author objects with all related books
        - Provide a complete view of an author and their works
        - Handle the one-to-many relationship in serialization
    
    Fields:
        id (int): Auto-generated primary key (read-only)
        name (str): Author's full name (required, max 200 chars)
        books (list): Nested list of Book objects (read-only)
    
    How the Nested Relationship Works:
        
        1. RELATIONSHIP IN MODEL:
           - Book model has: author = ForeignKey(Author, related_name='books')
           - This creates a reverse relationship from Author to Book
           - Access books via: author_instance.books.all()
        
        2. SERIALIZER IMPLEMENTATION:
           - books field uses BookSerializer to serialize each book
           - many=True: Indicates multiple book instances (one-to-many)
           - read_only=True: Books are displayed but not created via this serializer
        
        3. SERIALIZATION FLOW:
           When serializing an Author:
           a) AuthorSerializer serializes the author's id and name
           b) It finds all related books using author.books.all()
           c) Each book is serialized using BookSerializer
           d) The serialized books are included in the 'books' field
        
        4. RESULT:
           Single API call returns author with ALL their books nested inside
    
    Read-Only vs Writable:
        - books field is read_only=True
        - This means you CANNOT create books through AuthorSerializer
        - To create books, use BookSerializer directly
        - This prevents nested writes which can be complex
    
    Usage Example:
        # Serialize an author with all their books
        author = Author.objects.get(id=1)
        serializer = AuthorSerializer(author)
        
        # Result includes nested books:
        # {
        #     "id": 1,
        #     "name": "J.K. Rowling",
        #     "books": [
        #         {"id": 1, "title": "Harry Potter...", "publication_year": 1997, "author": 1},
        #         {"id": 2, "title": "Harry Potter...", "publication_year": 1998, "author": 1}
        #     ]
        # }
    """
    
    # NESTED SERIALIZER FIELD
    # This is the key to handling the Author-Book relationship
    books = BookSerializer(
        many=True,       # One author has MANY books (list of books)
        read_only=True   # Only for reading, not for creating/updating
    )
    # The field name 'books' matches the related_name='books' in Book.author ForeignKey
    # Django automatically uses author.books.all() to get related books
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Include the nested 'books' field
    
    # Note: We don't need to override create() or update() methods because
    # the books field is read_only. If we wanted writable nested serialization,
    # we would need to implement custom create() and update() methods.