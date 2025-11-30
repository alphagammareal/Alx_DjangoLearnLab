from rest_framework import serializers
from .models import Author, Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Handles serialization of all Book fields and includes custom validation
    to ensure the publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__'  # Serialize all fields: id, title, publication_year, author

    def validate_publication_year(self, value):
        """
        Custom validation: Ensure publication year is not greater than the current year.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes the author's name and a nested representation of related books
    using BookSerializer. The 'books' field is read-only and dynamically fetches
    all books linked to the author via the foreign key relationship.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serializer for related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  # Serialize id, name, and nested books