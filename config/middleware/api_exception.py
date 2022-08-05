from datetime import datetime

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from config.settings import logger


def custom_exception_handler(exc, context):
    logger.error(f"[CUSTOM_EXCEPTION_HANDLER_ERROR]")
    logger.error(f"[{datetime.now()}]")
    logger.error(f"> exc")
    logger.error(f"{exc}")
    logger.error(f"> context")
    logger.error(f"{context}")

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.PermissionDenied):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            code = response.status_code
            msg = exc.detail
        else:
            code = response.status_code
            msg = "unknown error"

        response.status_code = 200
        response.data['code'] = code
        response.data['message'] = msg
        response.data['data'] = None

        response.data.pop('detail', None)
        return response
    else:
        return Response({
            "code": "internal-error",
            "default_message": "unknown error occurred.",
        }, status=200)
