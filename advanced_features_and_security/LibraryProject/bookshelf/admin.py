from django.contrib import admin
from .models import Book

# Register the Book model with custom admin configuration
class BookAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters in the right sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search capability
    search_fields = ('title', 'author')

# Register the Book model with the custom admin class
admin.site.register(Book, BookAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    Extends Django's built-in UserAdmin to include our custom fields.
    """
    model = CustomUser
    
    # Fields to display in the user list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff']
    
    # Add our custom fields to the user detail/edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    
    # Add our custom fields to the "Add User" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register the CustomUser with our CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
