import requests
import ujson

OWNER_ID = '-86678270'
API_URL = 'https://api.vk.com/method/'
WALL_GET_METHOD = 'wall.get'
USER_INFO_METHOD = 'users.get'
CITY_GET_METHOD = 'database.getCitiesById'
API_VERSION = '5.63'
DEFAULT_MESSAGE = 'Not available'


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
            # First element is count of posts, so we exclude it
            try:
                posts_dic = response_dic['response'][1:]
            except IndexError:
                break
            for elem in posts_dic:
                self.posts.append(Post(elem))
            wall_get_params['offset'] += 100
            print(posts_dic)

    def __init__(self, owner_id):
        self.id = owner_id
        self.download_posts()


class User(object):

    def __init__(self, id):
        self.id = id
        self.age = DEFAULT_MESSAGE
        self.city = DEFAULT_MESSAGE
        self.get_user_info()

    def get_user_info(self):
        user_params = {'user_ids': self.id, 'fields': 'city,bdate', 'version': API_VERSION}
        vk_structure = get_resp_with_method(API_URL, USER_INFO_METHOD, user_params)
        print(vk_structure)
        vk_structure = vk_structure['response'][0]
        date_struct = vk_structure['bdate'].split('.')
        city_id = vk_structure['city']
        date_len = len(date_struct)
        if date_len == 3:
            self.age = date_struct[2]
        self.get_city_by_id(city_id)

    def get_city_by_id(self, city_id):
        user_params = {'city_ids': city_id, 'version': API_VERSION}
        vk_structure = get_resp_with_method(API_URL, CITY_GET_METHOD, user_params)
        vk_structure = vk_structure['response'][0]
        print(vk_structure)
        city_str = vk_structure['name']
        self.city = city_str


class Comment(object):

    def __init__(self, comment_id, post, text, author):
        self.id = comment_id
        self.post = post
        self.text = text
        self.author = author


class Post(object):

    def __init__(self, vk_structure):
        print(vk_structure)
        self.text = vk_structure['text']
        self.post_id = vk_structure['id']
        self.owner_id = vk_structure['to_id']
        try:
            self.signer = User(vk_structure['signer_id'])
        except KeyError:
            self.signer = DEFAULT_MESSAGE

if __name__ == '__main__':
    VkGroup(OWNER_ID)