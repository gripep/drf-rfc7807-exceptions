from rest_framework.settings import api_settings as drf_api_settings

from .settings import api_settings
from .utils import camelize

CAMELIZE = api_settings.CAMELIZE


def handle_exc_detail_as_dict(data: dict, exc_detail: dict):
    invalid_params = []
    non_field_errors = []
    for field, error in exc_detail.items():
        error_detail = {}

        reason = error if not isinstance(error, list) or len(error) > 1 else error[0]

        if field == drf_api_settings.NON_FIELD_ERRORS_KEY:
            if isinstance(reason, list):
                non_field_errors.extend(reason)
            else:
                non_field_errors.append(reason)
        else:
            error_detail["name"] = field if not CAMELIZE else camelize(field)
            # TODO: unify reason to return either `str` or `list`
            error_detail["reason"] = reason
            invalid_params.append(error_detail)

    if invalid_params:
        data["invalid_params"] = invalid_params

    if non_field_errors:
        data["detail"] = non_field_errors


def handle_exc_detail_as_list(data: dict, exc_detail: list):
    detail = []
    for error in exc_detail:
        detail.append(error if not isinstance(error, list) else error[0])

    data["detail"] = detail
