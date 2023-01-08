# Django Rest Framework Problem Detail Exceptions

## What is this?

A library for [Django Rest Framework](https://www.django-rest-framework.org/) returning consistent and easy-to-parse error messages.

This library has been implemented using [RFC7807](https://tools.ietf.org/html/rfc7807) guidelines. It defines a "problem detail" as a way to include machine-readable error details in an HTTP response without having to define new error response formats for HTTP APIs.

This library was designed to be used by anyone, therefore all of the advanced "problem detail" components are optional.
Errors, on the other hand, are always formatted with DRF exception information formatted with RFC7807 keywords.

Companies like Twitter use RFC7807 to format their API error messages, e.g. [Twitter API response codes and errors](https://developer.twitter.com/en/support/twitter-api/error-troubleshooting).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Exception Handler](#exception-handler)
  - [Example JSON Error Responses](#example-json-error-responses)
  - [Settings](#settings)
    - [EXTRA_HANDLERS](#extra_handlers)
    - [CAMELIZE](#camelize)
- [Testing](#testing)
- [Support](#support)
- [Contributing](#contributing)

## Installation

Install using the command line:

```
pip install drf-problem-detail-exceptions
```

## Usage

### Exception Handler

Add `EXCEPTION_HANDLER` in your `REST_FRAMEWORK` settings of your Django project settings file:

```python
REST_FRAMEWORK = {
    # ...
    "EXCEPTION_HANDLER": "rest_framework_exceptions.exception_handler",
}
```

### Raising RFC7807-like errors

_Coming soon..._

### Example JSON Error Responses

#### Field validation errors

```json
{
    "title": "Error message.",
    "invalid_params": [
        {
            "name": "field_name",
            "reason": [
                "error",
                // ...
            ]
        },
        ...
    ]
}
```

#### Non-fields validation errors

```json
{
  "title": "Error message.",
  "detail": [
    "error"
    // ...
  ]
}
```

### Other bad requests with no details

```json
{
  "title": "Error message."
}
```

## Settings

Default available settings:

```python
REST_FRAMEWORK_EXCEPTIONS = {
    "EXTRA_HANDLERS": []
    "CAMELIZE": False,
}
```

- #### EXTRA_HANDLERS

Support for exceptions that differ from the standard structure of the Django Rest Framework.

For instance, you may want to specify you own exception:

```python
class AuthenticationFailed(exceptions.AuthenticationFailed):
    def __init__(self, detail=None, code=None):
        """
        Builds a detail dictionary for the error to give more information
        to API users.
        """
        detail_dict = {"detail": self.default_detail, "code": self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict["detail"] = detail

        if code is not None:
            detail_dict["code"] = code

        super().__init__(detail_dict)
```

Use exception in code:

```python
def my_func():
    raise AuthenticationFailed(
        {
            "detail": _("Given token not valid for any token type"),
            "messages": [
                {
                    "metadata": "metadata_data",
                    "type": "type_name",
                    "message": "error message",
                }
            ],
        }
    )
```

This will result in:

```python
AuthenticationFailed(
    {
        "detail": "Error message.",
        "messages": [
            {
                "metadata": "metadata_data",
                "type": "type_name",
                "message": "error message",
            }
        ],
    }
)
```

You can handle this by creating a `handlers.py` file and specifying an handler for your use case:

```python
def handle_exc_custom_authentication_failed(exc):
    from path.to.my.exceptions import AuthenticationFailed

    if isinstance(exc, AuthenticationFailed):
        try:
            exc.detail = exc.detail["messages"][0]["message"]
        except (KeyError, IndexError):
            exc.detail = exc.detail["detail"]

    return exc
```

Then add it to the `EXTRA_HANDLERS` setting:

```python
REST_FRAMEWORK_EXCEPTIONS = {
    "EXTRA_HANDLERS": [
        "path.to.my.handlers.handle_exc_custom_authentication_failed",
        # ...
    ]
}
```

- #### CAMELIZE

Camel case support for Django Rest Framework Exceptions JSON error responses.

If `CAMELIZE` is set to `True`:

```json
{
  "title": "Error message.",
  "invalidParams": [
    {
      "name": "fieldName",
      "reason": [
        "error"
        // ...
      ]
    }
    // ...
  ]
}
```

## Testing

Install dependencies:

```
pip install -r requirements.txt
```

Run tests:

```
pytest test_project
```

## Support

Please [open an issue](https://github.com/gripep/drf-problem-detail-exceptions/issues/new).

## Contributing

Please use the [Github Flow](https://guides.github.com/introduction/flow/). In a nutshell, create a branch, commit your code, and open a pull request.
