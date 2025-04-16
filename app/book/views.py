from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .permissions import IsAdminUserOrReadOnly

'''
Books Functions
'''
from .models import Book
from .serializers import BookSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_books(request):
    try:
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([AllowAny])
def search_books(request):
    try:
        query = request.GET.get('query', '')

        books = Book.objects.all()
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def create_book(request):
    try:
        if not request.data: return Response({"detail": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_book(data, book):
    try:
        serializer = BookSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUserOrReadOnly])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def book_details(request, id):
    try:
        book = Book.objects.get(pk=id)

        if request.method == 'GET':
            return Response(BookSerializer(book).data, status=status.HTTP_200_OK)

        if request.method == "PUT":
            if not request.data: return Response({"detail": "No data"}, status=status.HTTP_400_BAD_REQUEST)
            return update_book(request.data, book)

        if request.method == "DELETE":
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Book.DoesNotExist:
        return Response({"detail": "Invalid book id"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
Reviews Functions
'''
from .models import Review
from .serializers import ReviewSerializer

from user.models import UserProfile

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def get_all_reviews(request):
    try:
        reviews = Review.objects.filter(user__id=request.user.id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def search_reviews(request):
    try:
        userId = request.user.id
        query = request.GET.get('query', '')

        reviews = Review.objects.filter(user__id=userId)

        if query:
            reviews = reviews.filter(
                Q(book__title__icontains=query) | Q(book__author__icontains=query)
            )

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def create_review(request):
    try:
        if not request.data: return Response({"detail": "No data"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['user_id'] = request.user.id
        request.data['user'] = request.user.id

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_review(data, review):
    try:
        serializer = ReviewSerializer(review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def review_details(request, id):
    try:
        review = Review.objects.get(id=id, user__id=request.user.id)

        if request.method == 'GET':
            return Response(ReviewSerializer(review).data, status=status.HTTP_200_OK)

        if request.method == "PUT":
            if not request.data: return Response({"detail": "No data"}, status=status.HTTP_400_BAD_REQUEST)
            request.data["user_id"] = request.user.id
            request.data["book_id"] = review.book.id
            return update_review(request.data, review)

        if request.method == "DELETE":
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    except Review.DoesNotExist:
        return Response({"detail": "Invalid review id"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"{str(e)}")
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
