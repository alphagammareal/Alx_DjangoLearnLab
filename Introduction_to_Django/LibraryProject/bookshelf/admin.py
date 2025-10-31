from django.contrib import admin
from .models import Book 

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year') #field shown in view list
    list_filter = ('publication_year',)  # Filter sidebar
    search_fields = ('title', 'author') # Enables search by title or author

admin.site.register(Book, BookAdmin)