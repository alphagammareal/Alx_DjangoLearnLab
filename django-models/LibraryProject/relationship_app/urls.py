from django.urls import path
from . import views  

urlpatterns = [
    # Home / index
    path('', views.index, name='index'),

    # Books list
    path('books/', views.list_books, name='book_list'),

    # Library detail view (class-based)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', views.UserLogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-based URLs
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

    # Book CRUD URLs
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
