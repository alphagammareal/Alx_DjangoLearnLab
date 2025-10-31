# delete.md

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Output:
# (1, {'bookshelf.Book': 1})
# <QuerySet []>  # confirms deletion
