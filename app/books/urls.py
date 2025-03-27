from django.urls import path
from .views import get_all_books, create_book, book_details, get_all_reviews, create_review, review_details

urlpatterns = [
    # Books routes
    path('', get_all_books, name='get_all_books'),
    path('create/', create_book, name='create_book'),
    path('<int:id>/', book_details, name='book_details'), # Get Book, Update Book, Delete Book
    
    # Reviews routes
    path('reviews/', get_all_books, name='get_all_books'),
    path('reviews/create/', create_book, name='create_book'),
    path('reviews/<int:id>/', book_details, name='book_details'), # Get Review, Update Review, Delete Review
]