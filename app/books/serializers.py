from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Books, Reviews

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'
    
    def validate(self, attrs):
        name = attrs.get('name')
        author = attrs.get('author')

        if self.instance and self.instance.name == name and self.instance.author == author:
            return attrs

        if Books.objects.filter(name=name, author=author).exists():
            raise ValidationError(
                _("This book has already been registered")
            )
        return attrs

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
    
    def validate(self, attrs):
        user = attrs.get('user')
        book = attrs.get('book')

        if self.instance and self.instance.user == user and self.instance.book == book:
            return attrs

        if Reviews.objects.filter(user=user, book=book).exists():
            raise ValidationError(
                _("User has already made a review for this book"),
                params={'value': [user, book]}
            )
        return attrs