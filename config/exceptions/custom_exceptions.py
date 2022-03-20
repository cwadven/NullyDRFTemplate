from rest_framework.exceptions import APIException


class CustomDictException(APIException):
    status_code = 200
    default_detail = 'unknown error.'
    default_code = 'unknown-error'