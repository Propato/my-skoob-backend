from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

'''
Books Functions
'''
from .models import Books
from .serializers import BooksSerializer

@api_view(["GET"])
def get_all_books(request):
    try:
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def create_book(request):
    try:
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def update_book(data, book):
    try:
        serializer = BooksSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"errors": f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET", "PUT", "DELETE"])
def book_details(request, id):
    try:
        book = Books.objects.get(pk=id)
    except Books.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == 'GET':
        return Response(BooksSerializer(book).data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        return update_book(request.data, book)

    if request.method == "DELETE":
        try:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''
Reviews Functions
'''
from .models import Reviews
from .serializers import ReviewsSerializer

@api_view(["GET"])
def get_all_reviews(request):
    try:
        reviews = Reviews.objects.all()
        serializer = ReviewsSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def create_review(request):
    try:
        serializer = ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def update_review(data, review):
    try:
        serializer = ReviewsSerializer(review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"errors": f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET", "PUT", "DELETE"])
def review_details(request, id):
    try:
        review = Reviews.objects.get(pk=id)
    except Reviews.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if request.method == 'GET':
        return Response(ReviewsSerializer(review).data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        return update_review(request.data, review)

    if request.method == "DELETE":
        try:
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
