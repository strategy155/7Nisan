import ujson
from urllib.parse import urlencode
from urllib.request import urlopen


def get_resp_with_method(api_url, method, params):
    api_request_url = api_url + method + urlencode(params)
    response = urlopen(api_request_url).read().decode()
    response_dic = ujson.loads(response)
    return response_dic