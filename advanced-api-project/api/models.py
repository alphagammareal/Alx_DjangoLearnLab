from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents an author of books.
    This model stores basic information about the author and serves as the parent
    in a one-to-many relationship with the Book model (one author can have many books).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    

class Book(models.Model):
    """
    Represents a book written by an author.
    This model includes details about the book and links to its author via a foreign key,
    enabling nested serialization of books under authors.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name= 'books')

    def __str__(self):
        return f"{self.title}"
