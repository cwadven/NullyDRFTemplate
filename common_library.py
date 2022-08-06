import uuid
import boto3 as boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.exceptions import APIException

from config.common.reponse_codes import PageSizeMaximumException


def mandatory_key(request, *args: str) -> dict:
    """
    args each type: string

    each dictionary string represent check request from key
    if there is not value raise Error

    example:
    mandatory_data = mandatory_key(request, "username", "password")

    returns:
    {'username': 'root', 'password': 'root'}
    """
    data_obj = dict()

    for key in args:
        try:
            data = request.GET[key]

            if request.method == 'GET':
                data_obj.update({key: data})
            else:
                data_obj.update({key: data})
            if data == "":
                raise APIException(f"missing mandatory key '{key}'")
        except:
            try:
                data = request.data[key]
                data_obj.update({key: data})
                if data == "":
                    raise APIException(f"missing mandatory key '{key}'")
            except:
                raise APIException(f"missing mandatory key '{key}'")

    return data_obj


def optional_key(request, *args: dict) -> dict:
    """
    args each type: dictionary -> {"key": value}

    each dictionary key represent check request from key
    each dictionary value represent default value if there is not value

    example:
    optional_data = optional_key(request, {"username": "123"}, {"password": "124"}, {"dd": 123})

    returns:
    {'username': 'root', 'password': 'root', 'dd': 123}
    """
    data_obj = dict()
    for arg in args:
        key, default_value = [[key, value] for key, value in arg.items()][0]
        try:
            data = request.GET[key]

            if data in ["", None, 'null', 'undefined']:
                data = default_value

            if request.method == 'GET':
                data_obj.update({key: data})
            else:
                data_obj.update({key: data})
        except:
            try:
                data = request.data[key]

                if data in ["", None, 'null', 'undefined']:
                    data = default_value

                data_obj.update({key: data})
            except:
                data = default_value
                data_obj.update({key: data})

    return data_obj


def paging(request, default_size=10):
    try:
        page = int(request.GET.get('page', 1)) - 1
        size = int(request.GET.get('size', default_size))
        if size > 30:
            raise PageSizeMaximumException()
        start_row = page * size
        end_row = (page + 1) * size
    except APIException as e:
        raise APIException(e)
    return start_row, end_row


def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def generate_presigned_url(file_name, expires_in=1000):
    s3_client = boto3.client(
        's3',
        region_name='ap-northeast-2',
        aws_access_key_id=settings.AWS_IAM_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_IAM_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4')
    )
    try:
        url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': settings.AWS_S3_BUCKET_NAME,
                'Key': f'{uuid.uuid4()}_{file_name}'
            },
            ExpiresIn=expires_in
        )
        return url
    except ClientError as e:
        raise APIException(e)


def send_email(title: str, html_body_content: str, payload: dict, to: list) -> None:
    """
    title: 메일 제목
    html_body_content: 적용할 templates 폴더에 있는 html 파일 위치
    payload: 해당 template_tag 로 쓰일 값들
    to: 보낼 사람들 (리스트로 전달 필요)
    """
    message = render_to_string(
        html_body_content,
        payload
    )
    send_mail(
        title,
        strip_tags(message),
        settings.EMAIL_HOST_USER,
        to,
        html_message=message,
        fail_silently=False,
    )
