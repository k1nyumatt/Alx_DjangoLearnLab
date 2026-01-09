# CRUD Operations Documentation

## 1. CREATE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
```

### Output:
```
1984
```

### Explanation:
Successfully created a Book instance with title "1984", author "George Orwell", and publication year 1949.

---

## 2. RETRIEVE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, Year: {book.publication_year}")
```

### Output:
```
Title: 1984, Author: George Orwell, Year: 1949
```

### Explanation:
Successfully retrieved the book and displayed all its attributes.

---

## 3. UPDATE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```

### Output:
```
Nineteen Eighty-Four
```

### Explanation:
Successfully updated the book title from "1984" to "Nineteen Eighty-Four".

---

## 4. DELETE Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
```

### Output:
```
(1, {'bookshelf.Book': 1})
<QuerySet []>
```

### Explanation:
Successfully deleted the book. The QuerySet is empty, confirming the deletion.