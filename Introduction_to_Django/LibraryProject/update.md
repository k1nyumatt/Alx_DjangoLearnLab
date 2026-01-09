# Update Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```

## Output:
```
Nineteen Eighty-Four
```

Successfully updated the book title from "1984" to "Nineteen Eighty-Four".