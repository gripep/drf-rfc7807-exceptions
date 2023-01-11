import logging
from typing import Dict, List, Union

from django.core.exceptions import (
    PermissionDenied,
    ValidationError as DjangoValidationError,
)
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import set_rollback

from .handlers import handle_exc_detail_as_dict, handle_exc_detail_as_list
from .settings import api_settings

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default this handles any REST framework `APIException`, and also
    Django's built-in `ValidationError`, `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions will log the exception message, and
    will cause a 500 error response.
    """

    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    extra_handlers = api_settings.EXTRA_HANDLERS
    if extra_handlers:
        for handler in extra_handlers:
            handler(exc)

    # unhandled exceptions, which should raise a 500 error and log the exception
    if not isinstance(exc, exceptions.APIException):
        logger.exception(exc)
        data = {"title": "Server error."}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # from DRF
    # https://github.com/encode/django-rest-framework/blob/48a21aa0eb3a95d32456c2a927eff9552a04231e/rest_framework/views.py#L87-L91
    headers = {}
    if getattr(exc, "auth_header", None):
        headers["WWW-Authenticate"] = exc.auth_header  # type: ignore
    if getattr(exc, "wait", None):
        headers["Retry-After"] = "%d" % exc.wait  # type: ignore

    data = {}
    if isinstance(exc.detail, (list, dict)) and isinstance(
        exc, exceptions.ValidationError
    ):
        data["title"] = "Validation error."
        _add_exc_detail_to_data(data, exc.detail)
    else:
        data = {"title": exc.detail}

    set_rollback()
    return Response(data, status=exc.status_code, headers=headers)


def _add_exc_detail_to_data(data: Dict, exc_detail: Union[Dict, List]) -> Dict:
    logger.debug("`exc_detail` is instance of %s" % type(exc_detail))

    if isinstance(exc_detail, dict):
        handle_exc_detail_as_dict(data, exc_detail)
    elif isinstance(exc_detail, list):
        handle_exc_detail_as_list(data, exc_detail)

    return data
