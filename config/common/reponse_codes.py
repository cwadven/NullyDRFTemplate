from rest_framework.exceptions import APIException


class PageSizeMaximumException(APIException):
    status_code = 400
    default_detail = '사이즈를 초과했습니다.'
    default_code = 'page-size-maximum'
