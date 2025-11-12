from django.contrib import admin
from .models import Book 
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year') #field shown in view list
    list_filter = ('publication_year',)  # Filter sidebar
    search_fields = ('title', 'author') # Enables search by title or author

# Register your models here.

# Custom admin configuration
class CustomUserAdmin(UserAdmin):
    # Add the new fields to the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_picture')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_picture')}),
    )

    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)