from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Library
from django.views.generic import DetailView

def index(request):
    return HttpResponse("Welcome to the Relationship App!")

def book_list(request):
    """A view that displays a simple text list of book titles and authors."""
    books = Book.objects.all()
    output = "\n".join([f"{book.title} - {book.author.name}" for book in books])
    return HttpResponse(output, content_type="text/plain")


class LibraryDetailView(DetailView):
    """A class-based view for displaying details of a specific library and its books."""
    model = Library
    template_name = 'books/library_detail.html'
    context_object_name = 'library'  # how it will be referred to in the template
