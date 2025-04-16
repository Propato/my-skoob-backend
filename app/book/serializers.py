from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Book, Review
from user.models import UserProfile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):
        title = attrs.get('title')
        author = attrs.get('author')

        if self.instance and self.instance.title == title and self.instance.author == author:
            return attrs

        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError({
                "Book": _("This book has already been registered"),
            })
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)

    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=UserProfile.objects.all())

    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'user': {'write_only': True},
            'status': {'write_only': True},
        }

    def validate(self, attrs):
        user = attrs.get('user')
        book = attrs.get('book')

        if self.instance and self.instance.user == user and self.instance.book == book:
            return attrs

        if Review.objects.filter(user=user, book=book).exists():
            raise ValidationError({
                "Review": _("User has already made a review for this book")
            })
        return attrs