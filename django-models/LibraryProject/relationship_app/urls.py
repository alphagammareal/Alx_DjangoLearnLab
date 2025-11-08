from django.urls import path
from .views import list_books, LibraryDetailView, index, user_login, user_logout, register

urlpatterns = [
    path('', index, name='index'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
