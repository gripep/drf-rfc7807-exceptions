from django.contrib.auth import get_user_model

import factory
from faker import Faker

from test_app.models import Book, Library

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyAttribute(lambda _: faker.unique.user_name())

    class Meta:
        model = get_user_model()


class BookFactory(factory.django.DjangoModelFactory):
    # slice not to exceed max_length
    title = factory.LazyAttribute(lambda _: faker.word()[:32])
    pages = factory.LazyAttribute(lambda _: faker.pyint(max_value=360))
    isbn10 = factory.LazyAttribute(lambda _: faker.unique.isbn10())

    class Meta:
        model = Book


class LibraryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Library
