import copy
from typing import Dict, List

from rest_framework.settings import api_settings as drf_api_settings

from .settings import api_settings
from .utils import camelize, flatten_dict


def handle_exc_detail_as_dict(data: Dict, exc_detail: Dict):
    exc_detail = flatten_dict(copy.deepcopy(exc_detail))

    invalid_params = []
    non_field_errors = []
    for field, error in exc_detail.items():
        error_detail = {}

        reason = error if not isinstance(error, list) or len(error) > 1 else error[0]

        if field in {drf_api_settings.NON_FIELD_ERRORS_KEY, "__all__"}:
            if isinstance(reason, list):
                non_field_errors.extend(reason)
            else:
                non_field_errors.append(reason)
        else:
            error_detail["name"] = (
                field if not api_settings.CAMELIZE else camelize(field)
            )
            if isinstance(reason, list):
                error_detail["reason"] = reason
            else:
                error_detail["reason"] = [reason]

            invalid_params.append(error_detail)

    if invalid_params:
        data["invalid_params"] = invalid_params

    if non_field_errors:
        data["detail"] = non_field_errors


def handle_exc_detail_as_list(data: Dict, exc_detail: List):
    detail = []
    for error in exc_detail:
        detail.append(error if not isinstance(error, list) else error[0])

    data["detail"] = detail
