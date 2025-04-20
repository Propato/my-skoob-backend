from django.contrib import admin
from .models import Book, Review


class BookAdmin(admin.AdminSite):
    site_header = "Books Admin Area"


bookAdmin = BookAdmin(name="BooksAdmin")
bookAdmin.register(Book)


class ReviewAdmin(admin.AdminSite):
    site_header = "Reviews Admin Area"


reviewAdmin = ReviewAdmin(name="ReviewsAdmin")
reviewAdmin.register(Review)
