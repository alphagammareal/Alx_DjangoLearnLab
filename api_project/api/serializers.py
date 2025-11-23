
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# the above is a serializer to convert Book model instances into JSON format and includes all fields of the Book model.