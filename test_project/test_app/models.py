from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from test_app.utils import ErrorTriggers


class Book(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="books", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=32)
    pages = models.IntegerField()
    isbn10 = models.CharField(max_length=13, unique=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                # one page a day keeps the errors away ;)
                name="%(app_label)s_%(class)s_pages_lte_360",
                check=models.Q(pages__lte=360),
            )
        ]

    def clean(self):
        super().clean()

        if self.title == ErrorTriggers.MODEL_VALIDATION.value:
            raise ValidationError(ErrorTriggers.MODEL_VALIDATION)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)


class Library(models.Model):
    name = models.CharField(max_length=32)
    books = models.ManyToManyField(Book)
