# Retrieve Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

## Output:
```
Title: 1984, Author: George Orwell, Year: 1949
```

Successfully retrieved the book with all its attributes.