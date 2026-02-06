# Advanced API Project - Book Management API

## Project Overview
A RESTful API built with Django REST Framework for managing a book library. Implements CRUD operations using DRF's generic views with role-based permissions.

## Features
- List all books (public access)
- View book details (public access)
- Create new books (authenticated users only)
- Update existing books (authenticated users only)
- Delete books (authenticated users only)

## Technology Stack
- Django 4.x
- Django REST Framework 3.x
- SQLite (default database)
- Token Authentication

## Project Structure
```
advanced-api-project/
├── api/
│   ├── models.py          # Book model definition
│   ├── serializers.py     # BookSerializer for JSON conversion
│   ├── views.py           # Generic views for CRUD operations
│   └── urls.py            # API endpoint routing
├── advanced_api_project/
│   ├── settings.py        # Project configuration
│   └── urls.py            # Main URL routing
└── manage.py
```

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Alx_DjangoLearnLab/advanced-api-project
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install django djangorestframework
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/api/books/` | List all books | No |
| GET | `/api/books/<id>/` | Get book details | No |
| POST | `/api/books/create/` | Create new book | Yes |
| PUT | `/api/books/<id>/update/` | Full update of book | Yes |
| PATCH | `/api/books/<id>/update/` | Partial update of book | Yes |
| DELETE | `/api/books/<id>/delete/` | Delete book | Yes |

## Authentication

This API uses Token Authentication. To access protected endpoints:

### 1. Obtain a token
```bash
# First, create a token for your user via Django shell
python manage.py shell

>>> from django.contrib.auth.models import User
>>> from rest_framework.authtoken.models import Token
>>> user = User.objects.get(username='your_username')
>>> token = Token.objects.create(user=user)
>>> print(token.key)
```

### 2. Use token in requests
Include the token in the Authorization header:
```
Authorization: Token YOUR_TOKEN_HERE
```

## Testing the API

### Using curl

**List all books (no authentication needed):**
```bash
curl http://localhost:8000/api/books/
```

**Get single book:**
```bash
curl http://localhost:8000/api/books/1/
```

**Create a book (authentication required):**
```bash
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Beginners",
    "author": "William S. Vincent",
    "publication_year": 2022,
    "isbn": "9781735467221"
  }'
```

**Update a book:**
```bash
curl -X PUT http://localhost:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django for Professionals",
    "author": "William S. Vincent",
    "publication_year": 2023,
    "isbn": "9781735467238"
  }'
```

**Partial update (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"publication_year": 2024}'
```

**Delete a book:**
```bash
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Using Postman

1. **Set up authentication:**
   - Go to Authorization tab
   - Select "API Key" type
   - Key: `Authorization`
   - Value: `Token YOUR_TOKEN_HERE`

2. **Test endpoints:**
   - GET `http://localhost:8000/api/books/`
   - POST `http://localhost:8000/api/books/create/` with JSON body

## View Configurations

### BookListView (generics.ListAPIView)
- **Purpose:** Retrieve all books
- **Permission:** AllowAny
- **Queryset:** All Book objects
- **Features:** Returns paginated list of books

### BookDetailView (generics.RetrieveAPIView)
- **Purpose:** Retrieve single book by ID
- **Permission:** AllowAny
- **Lookup:** Primary key (pk)

### BookCreateView (generics.CreateAPIView)
- **Purpose:** Create new book
- **Permission:** IsAuthenticated
- **Validation:** Custom publication_year validation in serializer
- **Hook:** `perform_create()` for custom creation logic

### BookUpdateView (generics.UpdateAPIView)
- **Purpose:** Update existing book
- **Permission:** IsAuthenticated
- **Methods:** PUT (full update), PATCH (partial update)
- **Hook:** `perform_update()` for custom update logic

### BookDeleteView (generics.DestroyAPIView)
- **Purpose:** Delete book
- **Permission:** IsAuthenticated
- **Hook:** `perform_destroy()` for custom deletion logic

## Permissions System

The API uses DRF's built-in permission classes:

- **`permissions.AllowAny`**: No authentication required (read operations)
- **`permissions.IsAuthenticated`**: Requires valid token (write operations)

This implements a "read-only for public, write for authenticated" pattern.

## Data Validation

The `BookSerializer` includes:
- **Field-level validation:** `validate_publication_year()` ensures year is between 1000-2100
- **Object-level validation:** `validate()` method for cross-field validation
- **Automatic validation:** Required fields, max_length, unique constraints

## Future Enhancements
- [ ] Add filtering and search capabilities
- [ ] Implement pagination
- [ ] Add user-specific permissions (owner-only updates)
- [ ] Add soft delete functionality
- [ ] Implement API versioning
- [ ] Add comprehensive unit tests

## License
This project is for educational purposes as part of ALX Django Learning Lab.

## Author
[Your Name]

## Advanced Query Capabilities

The Book API supports filtering, searching, and ordering to help you find exactly what you need.

### Filtering

Filter books by exact or partial matches on specific fields.

**Available Filters:**
- `title` - Filter by book title (case-insensitive partial match)
- `author` - Filter by author name (case-insensitive partial match)
- `publication_year` - Filter by exact publication year
- `publication_year__gte` - Filter books published on or after a year
- `publication_year__lte` - Filter books published on or before a year

**Examples:**
```bash
# Get all books by a specific author
GET /api/books/?author=John Doe

# Get books published in 2023
GET /api/books/?publication_year=2023

# Get books published after 2020
GET /api/books/?publication_year__gte=2020

# Get books from 2020-2023
GET /api/books/?publication_year__gte=2020&publication_year__lte=2023

# Multiple filters
GET /api/books/?author=Jane&publication_year=2024
```

### Searching

Perform text searches across multiple fields simultaneously.

**Search Fields:**
- `title` - Book title
- `author` - Author name

**Examples:**
```bash
# Search for "Django" in title or author
GET /api/books/?search=Django

# Search for "Python programming"
GET /api/books/?search=Python%20programming
```

### Ordering

Sort results by one or more fields.

**Available Ordering Fields:**
- `title` - Sort by book title
- `author` - Sort by author name
- `publication_year` - Sort by publication year

**Sort Direction:**
- Ascending: Use field name as-is (e.g., `title`)
- Descending: Prefix with `-` (e.g., `-title`)

**Examples:**
```bash
# Order by title A-Z
GET /api/books/?ordering=title

# Order by title Z-A
GET /api/books/?ordering=-title

# Order by newest first
GET /api/books/?ordering=-publication_year

# Order by year (newest), then title (A-Z)
GET /api/books/?ordering=-publication_year,title
```

### Combining Features

You can combine filtering, searching, and ordering in a single request.

**Examples:**
```bash
# Search for "Django", published after 2020, ordered by newest
GET /api/books/?search=Django&publication_year__gte=2020&ordering=-publication_year

# Filter by author, search in titles, order alphabetically
GET /api/books/?author=Vincent&search=Django&ordering=title

# Complex query
GET /api/books/?author=Smith&publication_year__gte=2022&search=Python&ordering=-publication_year
```

## Implementation Details

### Filter Backends
The API uses three Django REST Framework filter backends:

1. **DjangoFilterBackend** - Enables field-based filtering
2. **SearchFilter** - Enables text search across multiple fields
3. **OrderingFilter** - Enables result sorting

### Configuration
Located in `api/views.py`:
```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
filterset_class = BookFilter  # Custom filter with advanced options
search_fields = ['title', 'author']
ordering_fields = ['title', 'author', 'publication_year']
ordering = ['title']  # Default ordering
```

### Custom Filters
Advanced filtering is handled by `BookFilter` in `api/filters.py`:
- Case-insensitive partial matching for title and author
- Range filtering for publication years
- Exact matching for publication year

### Search Behavior
- Searches are case-insensitive
- Searches across both title and author fields simultaneously
- Partial matches are returned

### Ordering Behavior
- Default ordering: alphabetical by title (A-Z)
- Multiple fields can be specified (comma-separated)
- Descending order: prefix field with `-`

## Quick API Reference

| Feature | Parameter | Example |
|---------|-----------|---------|
| **Filter by title** | `?title=<value>` | `?title=Django` |
| **Filter by author** | `?author=<value>` | `?author=Smith` |
| **Filter by year** | `?publication_year=<year>` | `?publication_year=2023` |
| **Year from** | `?publication_year__gte=<year>` | `?publication_year__gte=2020` |
| **Year to** | `?publication_year__lte=<year>` | `?publication_year__lte=2023` |
| **Search** | `?search=<query>` | `?search=Python` |
| **Order ascending** | `?ordering=<field>` | `?ordering=title` |
| **Order descending** | `?ordering=-<field>` | `?ordering=-publication_year` |
| **Multiple ordering** | `?ordering=<field1>,<field2>` | `?ordering=-publication_year,title` |