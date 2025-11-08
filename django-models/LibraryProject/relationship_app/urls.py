from django.urls import path
from .views import list_books, LibraryDetailView, index

urlpatterns = [
    path('', index, name='index'),  # Home page
    path('books/', list_books, name='book_list'),  # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
]
