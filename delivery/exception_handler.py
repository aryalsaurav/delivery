from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed,NotAuthenticated


def custom_exception_handler(exc,context):
    response = exception_handler(exc,context)

    if isinstance(exc,AuthenticationFailed):
        response.data = {
            "status": response.status_code,
            "message": "You need to log in to access this resource.",
            "error_code": "AUTH_ERROR",
        }
    if isinstance(exc,NotAuthenticated):
        response.data = {
            "status": response.status_code,
            "message": "You need to log in to access this resource.",
            "error_code": "AUTH_ERROR",
        }

        return response
