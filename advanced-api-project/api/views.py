# api/views.py

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author']
    ordering_fields = ['published_date', 'title']
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # For /books/update/ without pk in URL, we need to get pk from data
        book_id = serializer.validated_data.get('id') or self.request.data.get('id')
        if not book_id:
            return Response({"error": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prevent updating published_date if already set
        if 'published_date' in serializer.validated_data and instance.published_date:
            return Response({"error": "Cannot update published date"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(instance, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        book_id = self.request.data.get('id')
        if not book_id:
            raise serializers.ValidationError("ID is required for deletion")
        try:
            return Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise NotFound("Book not found")