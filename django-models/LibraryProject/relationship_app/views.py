from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

# Authentication imports required by checker
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Home page
def index(request):
    return HttpResponse("Welcome to the Relationship App!")

# Function-based view for listing books
def list_books(request):
    """A view that displays a simple text list of book titles and authors."""
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'relationship_app/list_books.html', context)

# Class-based view for library details
class LibraryDetailView(DetailView):
    """A class-based view for displaying details of a specific library and its books."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
