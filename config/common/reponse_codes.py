from rest_framework.exceptions import APIException


class PageSizeMaximumException(APIException):
    status_code = 400
    default_detail = '사이즈를 초과했습니다.'
    default_code = 'page-size-maximum'


class LoginFailedException(APIException):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'
