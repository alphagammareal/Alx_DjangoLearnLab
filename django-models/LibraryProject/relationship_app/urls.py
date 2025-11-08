from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.list_books, name='book_list'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', views.UserLogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]

 # Role-based URLs
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),