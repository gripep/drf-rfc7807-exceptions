from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class RFC7807Error(APIException):
    def __init__(self):
        raise NotImplementedError()


class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Server error.")
    default_code = "internal_server_error"
