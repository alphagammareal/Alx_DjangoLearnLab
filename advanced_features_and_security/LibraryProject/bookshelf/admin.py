from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


# ============================
#  Book Admin Configuration
# ============================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')   # fields shown in list view
    list_filter = ('publication_year',)                      # filter sidebar
    search_fields = ('title', 'author')                      # search bar for title/author


# ============================
#  Custom User Admin
# ============================
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    
    # Add custom fields to the existing Django UserAdmin fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_picture'),
        }),
    )

    # Fields displayed when creating a new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_picture'),
        }),
    )

    list_display = ('username', 'email', 'date_of_birth', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
