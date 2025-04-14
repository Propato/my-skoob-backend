from django.urls import path
from .views import get_all_books, search_books, create_book, book_details, get_all_reviews, create_review, review_details
from .admin import bookAdmin, reviewAdmin

urlpatterns = [
    # Books routes
    path('', get_all_books, name='get_all_books'),
    path('search/', search_books, name='search_books'),
    path('create/', create_book, name='create_book'),
    path('<int:id>/', book_details, name='book_details'), # Get Book, Update Book, Delete Book

    path('admin/', bookAdmin.urls),

    # Reviews routes
    path('reviews/', get_all_reviews, name='get_all_reviews'),
    path('reviews/create/', create_review, name='create_review'),
    path('reviews/<int:id>/', review_details, name='review_details'), # Get Review, Update Review, Delete Review

    path('reviews/admin/', reviewAdmin.urls),
]