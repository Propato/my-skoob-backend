from django.db import models
from django.core.validators import MaxValueValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import UserProfile


def validate_release_year(value):
    from datetime import date

    current_year = date.today().year
    if value > current_year:
        raise ValidationError(
            _(f"Please enter a year before {current_year}."),
            params={"value": value},
        )


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=120)
    overview = models.CharField(max_length=300)
    author = models.CharField(max_length=80)
    pages = models.IntegerField(null=True, blank=True)
    release_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[validate_release_year],
    )
    validate = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_book",
                violation_error_message=_("This book has already been registered"),
            )
        ]

    def __str__(self):
        return f"{self.author}:{self.title}:{self.release_year} - {self.validate}"


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    stars = models.IntegerField(
        null=True, blank=True, validators=[MaxValueValidator(100)]
    )
    comment = models.CharField(max_length=300, null=True, blank=True)

    STATUS = [
        (0, "Read"),
        (1, "Reading"),
        (2, "Drop"),
        (3, "List"),
    ]
    status = models.IntegerField(choices=STATUS, default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "book"],
                name="unique_user_review_per_book",
                violation_error_message=_(
                    "User has already made a review for this book"
                ),
            )
        ]

    def __str__(self):
        return f"[{self.user}]:[{self.book}]\n\t{self.get_status_display()} - {self.stars} - {self.comment}"
