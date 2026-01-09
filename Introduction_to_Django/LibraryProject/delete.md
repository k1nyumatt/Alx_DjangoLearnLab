# Delete Operation

## Command:
```python
from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
Book.objects.all()
```

## Output:
```
(1, {'bookshelf.Book': 1})
<QuerySet []>
```

Successfully deleted the book. The query returns an empty QuerySet confirming deletion.