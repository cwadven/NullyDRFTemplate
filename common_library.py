from rest_framework.exceptions import APIException


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
