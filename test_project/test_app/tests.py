from django.core.exceptions import PermissionDenied, ValidationError
from django.db.utils import IntegrityError
from django.http import Http404
from rest_framework import exceptions

import pytest

from drf_problem_detail_exceptions import exception_handler
from test_app.utils import ErrorTriggers, render_response


@pytest.mark.django_db
class TestErrors:
    def test_django_http404_ok(self, mocker):
        exc = Http404()
        response = exception_handler(exc, mocker.Mock())

        expected_response = {"title": "Not found."}
        assert render_response(response.data) == expected_response  # type: ignore

    def test_django_permission_denied_ok(self, mocker):
        exc = PermissionDenied()
        response = exception_handler(exc, mocker.Mock())

        expected_response = {
            "title": "You do not have permission to perform this action."
        }
        assert render_response(response.data) == expected_response  # type: ignore

    # ? TODO: Fix empty error messages cases
    @pytest.mark.parametrize(
        "error_message, expected_response",
        [
            # ("", {"title": "Validation error."}),
            # ([], {"title": "Validation error."}),
            # ([""], {"title": "Validation error."}),
            # ({}, {"title": "Validation error."}),
            # ({"": ""}, {"title": "Validation error."}),
            # ({"field": ""}, {"title": "Validation error."}),
            (
                "Error message.",
                {"title": "Validation error.", "detail": ["Error message."]},
            ),
            (
                [f"Error message {i}." for i in range(2)],
                {
                    "title": "Validation error.",
                    "detail": ["Error message 0.", "Error message 1."],
                },
            ),
            (
                {"field": "Error message."},
                {
                    "title": "Validation error.",
                    "invalid_params": [{"name": "field", "reason": ["Error message."]}],
                },
            ),
        ],
    )
    def test_django_validation_error_ok(self, error_message, expected_response, mocker):
        exc = ValidationError(error_message)
        response = exception_handler(exc, mocker.Mock())

        assert render_response(response.data) == expected_response  # type: ignore

    # ? TODO: Fix empty error messages cases
    @pytest.mark.parametrize(
        "error_message, expected_response",
        [
            # ("", {"title": "Validation error."}),
            # ([], {"title": "Validation error."}),
            # ([""], {"title": "Validation error."}),
            # ({}, {"title": "Validation error."}),
            # ({"": ""}, {"title": "Validation error."}),
            # ({"field": ""}, {"title": "Validation error."}),
            (
                "Error message.",
                {"title": "A server error occurred.", "detail": ["Error message."]},
            ),
            (
                [f"Error message {i}." for i in range(2)],
                {
                    "title": "A server error occurred.",
                    "detail": ["Error message 0.", "Error message 1."],
                },
            ),
            (
                {"field": "Error message."},
                {
                    "title": "A server error occurred.",
                    "invalid_params": [{"name": "field", "reason": ["Error message."]}],
                },
            ),
            (
                {"field1": {"field2": "Error message."}},
                {
                    "title": "A server error occurred.",
                    "invalid_params": [
                        {"name": "field1.field2", "reason": ["Error message."]}
                    ],
                },
            ),
        ],
    )
    def test_drf_api_exception_ok(self, error_message, expected_response, mocker):
        exc = exceptions.APIException(error_message)
        response = exception_handler(exc, mocker.Mock())

        assert render_response(response.data) == expected_response  # type: ignore

    # ? TODO: Fix empty error messages cases
    @pytest.mark.parametrize(
        "error_message, expected_response",
        [
            # ("", {"title": "Validation error."}),
            # ([], {"title": "Validation error."}),
            # ([""], {"title": "Validation error."}),
            # ({}, {"title": "Validation error."}),
            # ({"": ""}, {"title": "Validation error."}),
            # ({"field": ""}, {"title": "Validation error."}),
            (
                "Error message.",
                {"title": "Validation error.", "detail": ["Error message."]},
            ),
            (
                [f"Error message {i}." for i in range(2)],
                {
                    "title": "Validation error.",
                    "detail": ["Error message 0.", "Error message 1."],
                },
            ),
            (
                {"field": "Error message."},
                {
                    "title": "Validation error.",
                    "invalid_params": [{"name": "field", "reason": ["Error message."]}],
                },
            ),
            (
                {"field1": {"field2": "Error message."}},
                {
                    "title": "Validation error.",
                    "invalid_params": [
                        {"name": "field1.field2", "reason": ["Error message."]}
                    ],
                },
            ),
            (
                {
                    "field1": {
                        "field2": {"field3": {"field4": {"field5": "Error message."}}}
                    }
                },
                {
                    "title": "Validation error.",
                    "invalid_params": [
                        {
                            "name": "field1.field2.field3.field4.field5",
                            "reason": ["Error message."],
                        }
                    ],
                },
            ),
            (
                {
                    "field1": {"field2": "Error message."},
                    "field3": {"field4": "Error message."},
                },
                {
                    "title": "Validation error.",
                    "invalid_params": [
                        {"name": "field1.field2", "reason": ["Error message."]},
                        {"name": "field3.field4", "reason": ["Error message."]},
                    ],
                },
            ),
            (
                {
                    "field1": {"field2": "Error message."},
                    "field3": {"field4": {"field5": "Error message."}},
                },
                {
                    "title": "Validation error.",
                    "invalid_params": [
                        {"name": "field1.field2", "reason": ["Error message."]},
                        {"name": "field3.field4.field5", "reason": ["Error message."]},
                    ],
                },
            ),
        ],
    )
    def test_drf_validation_error_ok(self, error_message, expected_response, mocker):
        exc = exceptions.ValidationError(error_message)
        response = exception_handler(exc, mocker.Mock())

        assert render_response(response.data) == expected_response  # type: ignore


@pytest.mark.django_db
class TestSerializerErrors:
    def test_serializer_field_required_error_ok(self, book_serializer, mocker):
        serializer = book_serializer(data={})
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "invalid_params": [
                    {
                        "name": "title",
                        "reason": ["This field is required."],
                    },
                    {
                        "name": "pages",
                        "reason": ["This field is required."],
                    },
                    {
                        "name": "isbn10",
                        "reason": ["This field is required."],
                    },
                ],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_serializer_field_validation_error_ok(
        self, book, book_serializer, faker, mocker
    ):
        data = {
            "title": faker.word()[:32],  # slice not to exceed max_length
            "pages": faker.pyint(max_value=360),
            "isbn10": book.isbn10,
        }

        serializer = book_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "invalid_params": [
                    {
                        "name": "isbn10",
                        "reason": [f"Book with isbn10 {book.isbn10} already exists."],
                    }
                ],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_serializer_validation_error_ok(self, book_serializer, faker, mocker):
        data = {
            "title": ErrorTriggers.SERIALIZER_VALIDATION.value,
            "pages": faker.pyint(max_value=360),
            "isbn10": faker.unique.isbn10(),
        }

        serializer = book_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "detail": [f"Title cannot be {ErrorTriggers.SERIALIZER_VALIDATION}"],
            }
            assert render_response(response.data) == expected_response  # type: ignore


@pytest.mark.django_db
class TestModelSerializerErrors:
    def test_model_serializer_bad_one_to_one_relationship_error_ok(
        self, book_model_serializer, faker, mocker
    ):
        username = faker.user_name()
        data = {
            "author": username,
            "title": faker.word()[:32],
            "pages": ErrorTriggers.MODEL_CONSTRAINT.value,
            "isbn10": faker.unique.isbn10(),
        }

        serializer = book_model_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "invalid_params": [
                    {
                        "name": "author",
                        "reason": [f"Object with username={username} does not exist."],
                    }
                ],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_model_serializer_bad_many_to_many_relationship_error_ok(
        self, book_model_serializer, faker, mocker, user
    ):
        library_name1, library_name2 = faker.word()[:32], faker.word()[:32]
        data = {
            "author": user.username,
            "title": faker.word()[:32],
            "pages": ErrorTriggers.MODEL_CONSTRAINT.value,
            "isbn10": faker.unique.isbn10(),
            "libraries": [library_name1, library_name2],
        }

        serializer = book_model_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "invalid_params": [
                    {
                        "name": "libraries",
                        "reason": [f"Object with name={library_name1} does not exist."],
                    }
                ],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_model_serializer_constraint_error_ok(
        self, book_model_serializer, faker, mocker, user
    ):
        data = {
            "author": user.username,
            "title": faker.word()[:32],
            "pages": ErrorTriggers.MODEL_CONSTRAINT.value,
            "isbn10": faker.unique.isbn10(),
        }

        serializer = book_model_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {"title": "Server error."}
            assert render_response(response.data) == expected_response  # type: ignore

    def test_model_serializer_field_required_error_ok(
        self, book_model_serializer, mocker
    ):
        serializer = book_model_serializer(data={})
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "invalid_params": [
                    {
                        "name": "author",
                        "reason": ["This field is required."],
                    },
                    {
                        "name": "isbn10",
                        "reason": ["This field is required."],
                    },
                    {
                        "name": "pages",
                        "reason": ["This field is required."],
                    },
                    {
                        "name": "title",
                        "reason": ["This field is required."],
                    },
                ],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_model_serializer_method_error_ok(
        self, book_model_serializer, faker, mocker, user
    ):
        data = {
            "author": user.username,
            "title": ErrorTriggers.SERIALIZER_METHOD.value,
            "pages": faker.pyint(max_value=360),
            "isbn10": faker.unique.isbn10(),
        }

        serializer = book_model_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "detail": [ErrorTriggers.SERIALIZER_METHOD.value],
            }
            assert render_response(response.data) == expected_response  # type: ignore

    def test_model_serializer_validation_error_ok(
        self, book_model_serializer, faker, mocker, user
    ):
        data = {
            "author": user.username,
            "title": ErrorTriggers.SERIALIZER_VALIDATION.value,
            "pages": faker.pyint(max_value=360),
            "isbn10": faker.unique.isbn10(),
        }

        serializer = book_model_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.ValidationError as exc:
            response = exception_handler(exc, mocker.Mock())

            expected_response = {
                "title": "Validation error.",
                "detail": [f"Title cannot be {ErrorTriggers.SERIALIZER_VALIDATION}"],
            }
            assert render_response(response.data) == expected_response  # type: ignore
