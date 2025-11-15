from django.urls import path
from . import views  # import views from the current app

urlpatterns = [
    path('', views.index, name='index'),  # example route
    path('', views.book_list, name='book_list'),
    path('add/', views.add_book, name='add_book'),
    path('<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),
]
