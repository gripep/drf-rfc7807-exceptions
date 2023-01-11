from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class RFC7807Error(APIException):
    def __init__(self):
        raise NotImplementedError()


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Bad Request.")
    default_code = "bad_request"


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Conflict.")
    default_code = "conflict"


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Server error.")
    default_code = "internal_server_error"
