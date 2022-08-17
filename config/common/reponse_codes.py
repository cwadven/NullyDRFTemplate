from rest_framework.exceptions import APIException


class PageSizeMaximumException(APIException):
    status_code = 400
    default_detail = '사이즈를 초과했습니다.'
    default_code = 'page-size-maximum'


class LoginFailedException(APIException):
    status_code = 400
    default_detail = '로그인에 실패했습니다.'
    default_code = 'login-error'


class BlackUserException(APIException):
    status_code = 400
    default_detail = '정지된 유저입니다.'
    default_code = 'inaccessible-user-login'


class DormantUserException(APIException):
    status_code = 400
    default_detail = '휴면상태의 유저입니다.'
    default_code = 'dormant-user-login'


class LeaveUserException(APIException):
    status_code = 400
    default_detail = '탈퇴상태의 유저입니다.'
    default_code = 'leave-user-login'
