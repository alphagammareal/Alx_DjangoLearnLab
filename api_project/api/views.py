from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookList(generics.ListAPIView):
    """
    GET /api/books/  -> returns list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# NEW: Full CRUD using ModelViewSet
class BookViewSet(viewsets.ModelViewSet):
    """
    Provides:
    - GET /books_all/          (list)
    - GET /books_all/<id>/     (retrieve)
    - POST /books_all/         (create)
    - PUT /books_all/<id>/     (update)
    - DELETE /books_all/<id>/  (destroy)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer