from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    index,
    register,
    UserLoginView,
    UserLogoutView
)

urlpatterns = [
    path('', index, name='index'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
