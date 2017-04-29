import pickle
import re
from definitions import OWNER_ID, API_URL, WALL_GET_METHOD, USER_INFO_METHOD, COMMENT_GET_METHOD, POSTS_COUNT, \
    API_VERSION
from utils import get_resp_with_method


class VkGroup(object):

    def _download_posts(self):
        self.posts = []
        _wall_get_params = {'owner_id': self.group_id, 'count': '100', 'v': API_VERSION, 'offset': 0}
        for i in range(0, POSTS_COUNT, 100):
            _response_structure = get_resp_with_method(API_URL, WALL_GET_METHOD, _wall_get_params)
            _posts_structures = _response_structure['response']['items']
            if len(_posts_structures) < 1:
                break
            for idx, elem in enumerate(_posts_structures):
                print(idx, _response_structure['response']['count'])
                self.posts.append(Post(elem))
                print(self.posts)
            _wall_get_params['offset'] += 100

    def __init__(self, owner_id):
        self.group_id = owner_id
        self._download_posts()


class User(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.age = None
        self.city = None
        self._set_user_info()

    def _set_user_info(self):
        user_params = {'user_ids': self.user_id, 'fields': 'city, bdate', 'v': API_VERSION}
        vk_structure = get_resp_with_method(API_URL, USER_INFO_METHOD, user_params)
        try:
            response_structure = vk_structure['response'][0]
            try:
                self._set_city(response_structure)
                self._set_date(response_structure)
            except KeyError:
                pass
        except IndexError:
            print(vk_structure)
            pass

    def _set_date(self, response_structure):
        date_structure = response_structure['bdate'].split('.')
        date_len = len(date_structure)
        if date_len == 3:
            self.age = date_structure[2]

    def _set_city(self, response_structure):
        self.city = response_structure['city']['title']


class Comment(object):

    def __init__(self, response_structure):
        self.text = response_structure['text']
        self.comm_id = response_structure['id']
        self.owner = User(response_structure['from_id'])


class Post(object):
    def __init__(self, response_structure):
        self.text = response_structure['text']
        self.post_id = response_structure['id']
        self.owner_id = response_structure['owner_id']
        try:
            self.signer = User(response_structure['signer_id'])
        except KeyError:
            self.signer = None
        self._download_comments()

    def _download_comments(self):
        self.comments = []
        comments_get_params = {'owner_id': self.owner_id, 'post_id': self.post_id, 'count': '100', 'v': API_VERSION, 'offset': 0, 'extended': 1}
        while True:
            response_dic = get_resp_with_method(API_URL, COMMENT_GET_METHOD, comments_get_params)
            comments_dic = response_dic['response']['items']
            if len(comments_dic) < 1:
                break
            for elem in comments_dic:
                self.comments.append(Comment(elem))
            comments_get_params['offset'] += 100


class VkGroupStats(object):

    def __init__(self, group_obj):
        self.group_obj = group_obj
        self._count_posts_mean_length()

    def _count_posts_mean_length(self):
        for post in self.group_obj.posts:
            print(post.text.split(' '))


if __name__ == '__main__':
    # cool_shit = VkGroup(OWNER_ID)
    # with open('cool_shit.pkl', 'wb') as f:
    #     pickle.dump(cool_shit, f)
    with open('cool_shit.pkl', 'rb') as f:
        cool_shit = pickle.load(f)
    VkGroupStats(cool_shit)