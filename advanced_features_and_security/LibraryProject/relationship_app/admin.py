from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile

# Register Author model
admin.site.register(Author)

# Register other models
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)