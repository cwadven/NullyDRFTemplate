from account.social_login_helper.social_login_helpers import KakaoSocialType, NaverSocialType, GoogleSocialType
from config.common.enums import IntValueSelector


class SocialTypeSelector(IntValueSelector):
    """
    데이터 베이스에 2, 3, 4 로 UserProvider 와 의미가 같아야 합니다.
    """
    KAKAO_SOCIAL_TYPE = (2, KakaoSocialType)
    NAVER_SOCIAL_TYPE = (3, NaverSocialType)
    GOOGLE_SOCIAL_TYPE = (4, GoogleSocialType)
