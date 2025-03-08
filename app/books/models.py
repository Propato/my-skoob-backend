from django.db import models
from django.core.validators import MaxValueValidator

from users.models import Users

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    pages = models.IntegerField(blank=True)
    release = models.DateField(blank=True)
    validate = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'author'], name='unique_book', violation_error_message="This book has already been registered")
        ]

    def __str__(self):
        return f'{self.author}:{self.name}:{self.release} - {self.validate}'

class Review(models.Model):
    userId = models.ForeignKey(Users, on_delete=models.CASCADE)
    bookId = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    stars = models.IntegerField(blank=True, validators=[MaxValueValidator(100)])
    comment = models.CharField(max_length=300, blank=True)

    STATUS = [
        (0, "Read"),
        (1, "Reading"),
        (2, "Drop"),
        (3, "List"),
    ]
    status = models.IntegerField(choices=STATUS)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['userId', 'bookId'], name='unique_user_review_per_book', violation_error_message="User has already made a review for this book")
        ]

    def __str__(self):
        return f'[{self.userId}]:[{self.bookId}]\n\t{self.get_status_display()} - {self.stars} - {self.comment}'