from rest_framework.views import exception_handler
from rest_framework.exceptions import (AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    NotFound,
)


def custom_exception_handler(exc,context):
    response = exception_handler(exc,context)
    if response is not None:
        if isinstance(exc,AuthenticationFailed):
            response.data = {
                "status": response.status_code,
                "message": "Invalid Token.",
                "error_code": "AUTH_ERROR",
            }


        elif isinstance(exc,NotAuthenticated):
            response.data = {
                "status": response.status_code,
                "message": "You need to log in to access this resource.",
                "error_code": "AUTH_ERROR",
            }

        elif isinstance(exc,PermissionDenied):
            response.data = {
                "status": response.status_code,
                "message": "You are not authorized to perform this action.",
                "error_code": "AUTH_ERROR",
            }

        elif isinstance(exc,NotFound):
            response.data = {
                "status": response.status_code,
                "message": exc.detail,
                "error_code": "AUTH_ERROR",
            }

    return response
