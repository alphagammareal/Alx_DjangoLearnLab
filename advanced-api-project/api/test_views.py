# api/test_views.py

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book
from django.contrib.auth.models import User


class BookAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a user for authenticated requests
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client = APIClient()
        
        # Create sample books
        Book.objects.create(title="Django for Beginners", author="ALpha Gamma", publication_year=2019)
        Book.objects.create(title="Python Crash Course", author="ALpha ALX", publication_year=2021)
        Book.objects.create(title="i am tired", author="John Dramani", publication_year=2020)

    def test_list_books(self):
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_search_books(self):
        url = '/api/books/?search=Django'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two Scoops + Django for Beginners

    def test_filter_by_author(self):
        url = '/api/books/?author=Eric Matthes'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['author'], 'Eric Matthes')

    def test_ordering_by_year(self):
        url = '/api/books/?ordering=-publication_year'
        response = self.client.get(url)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, [2021, 2020, 2019])  # descending

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        url = '/api/books/create/'
        data = {
            "title": "Test Driven Development with Python",
            "author": "Harry Percival",
            "publication_year": 2017
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        url = '/api/books/create/'
        data = {"title": "Hacker's Book", "author": "Anon"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass123')
        book = Book.objects.first()
        url = '/api/books/update/'
        data = {"id": book.id, "title": "UPDATED: Django for Pros"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertIn("UPDATED", book.title)

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass123')
        book = Book.objects.first()
        url = '/api/books/delete/'
        response = self.client.delete(url, {"id": book.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())