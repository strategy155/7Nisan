import requests
import ujson

OWNER_ID = '-86678270'
API_URL = 'https://api.vk.com/method/'
WALL_GET_METHOD = 'wall.get'
USER_INFO_METHOD = 'users.get'
WALL_GET_METHOD = 'wall.get'
API_VERSION = '5.63'

def get_resp_with_method(api_url, method, params):
    api_request_url = api_url + method
    response = requests.get(api_request_url, params)
    response_dic = ujson.loads(response.text)
    return response_dic


class VkGroup(object):
    posts = list()

    def download_posts(self):
        wall_get_params = {'owner_id': self.id, 'count': '100', 'version': API_VERSION, 'offset': 0}
        while True:
            response_dic = get_resp_with_method(API_URL, WALL_GET_METHOD, wall_get_params)
            posts_dic = response_dic['response'][1:]
            for elem in posts_dic:

            print(len(response_dic['response']))

        return None

    def __init__(self, owner_id):
        self.id = id
        self.download_posts()


class User(object):
    age = int()
    city = str()

    def __init__(self, signer_id):


class Comment(object):
    post = Post()


class Post(object):

    def __init__(self, owner_id, post_id, text, signer_id):
        self.id = post_id
        self.owner_id = owner_id
        self.text = text
        self.signer = User(signer_id)