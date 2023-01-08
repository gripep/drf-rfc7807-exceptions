from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, "REST_FRAMEWORK_EXCEPTIONS", {})

DEFAULTS = {
    "EXTRA_HANDLERS": [],
    "CAMELIZE": False,
}

# list of settings that may be in string import notation
IMPORT_STRINGS = ("EXTRA_HANDLERS", "CAMELIZE")

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
