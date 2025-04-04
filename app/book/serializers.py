from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Book, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, attrs):
        name = attrs.get('name')
        author = attrs.get('author')

        if self.instance and self.instance.name == name and self.instance.author == author:
            return attrs

        if Book.objects.filter(name=name, author=author).exists():
            raise ValidationError({
                "Book": _("This book has already been registered"),
            })
        return attrs

class ReviewSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Review
        fields = '__all__'

    def validate_status(self, value):
        if value.isdigit():
            value = int(value)
            if value not in dict(Review.STATUS).keys():
                raise serializers.ValidationError("Invalid status value.")
            return value

        status_map = {v: k for k, v in Review.STATUS}
        if value not in status_map:
            raise serializers.ValidationError("Invalid status value.")
        return status_map[value]
    
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