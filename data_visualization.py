import pickle
import matplotlib.pyplot as plt
from definitions import DATE, OWNER_ID
from vk_api import VkGroup, Post, User, Comment
from matplotlib import style
style.use('ggplot')


class VkGroupStats(object):

    def __init__(self, group_obj):
        self.group_obj = group_obj
        self._get_post_to_len()
        self._get_post_to_comment_len()

    def plot_city(self):
        coordinates = self._coordinates_city_to_len()
        self._plot_graph(coordinates, name='City', x_label='City', y_label='Length of text')

    def plot_age(self):
        coordinates = self._coordinates_age_to_len()
        self._plot_graph(coordinates, name='Age', x_label='Age', y_label='Length of text')

    def plot_post_len_to_comments_len(self):
        coordinates = self._coordinates_post_len_to_comment_len()
        self._plot_graph(coordinates, name='Length', x_label='Length of post', y_label='Length of comment')

    @staticmethod
    def _get_len_of_text(text):
        _words_raw = text.replace('\n', ' ').split(' ')
        _words_filtered = list(filter(None, _words_raw))
        return len(_words_filtered)

    def _coordinates_post_len_to_comment_len(self):
        y_coordinates = []
        x_coordinates = []
        self._get_post_len_to_comment_len()
        for key in self.post_len_to_comment_len:
            sum_of_lens = 0
            posts_count = len(self.post_len_to_comment_len[key])
            for elem in self.post_len_to_comment_len[key]:
                if elem is None:
                    posts_count -= 1
                    continue
                sum_of_lens += elem
            if posts_count == 0:
                continue
            x_coordinates.append(key)
            y_coordinates.append(int(sum_of_lens/posts_count))
        return x_coordinates, y_coordinates

    def _correspond_text_to_age(self, user, text):
        if user is None or user.age is None:
            return None
        current_age = DATE - int(user.age)
        self._age_to_len.setdefault(current_age, []).append(self._get_len_of_text(text))

    def _get_age_to_len(self):
        self._age_to_len = {}
        for post in self.group_obj.posts:
            self._correspond_text_to_age(post.signer, post.text)
            for comment in post.comments:
                self._correspond_text_to_age(comment.owner, comment.text)

    def _coordinates_age_to_len(self):
        y_coordinates = []
        x_coordinates = []
        self._get_age_to_len()
        for key in self._age_to_len:
            sum_of_lens = 0
            posts_count = len(self._age_to_len[key])
            for elem in self._age_to_len[key]:
                sum_of_lens += elem
            x_coordinates.append(key)
            y_coordinates.append(int(sum_of_lens/posts_count))
        return x_coordinates, y_coordinates

    def _correspond_text_to_city(self, user, text):
        if user is None or user.city is None:
            return None
        self._city_to_len.setdefault(user.city, []).append(self._get_len_of_text(text))

    def _get_city_to_len(self):
        self._city_to_len = {}
        for post in self.group_obj.posts:
            self._correspond_text_to_city(post.signer, post.text)
            for comment in post.comments:
                self._correspond_text_to_city(comment.owner, comment.text)

    def _coordinates_city_to_len(self):
        y_coordinates = []
        x_coordinates = []
        self._get_city_to_len()
        for key in self._city_to_len:
            sum_of_lens = 0
            posts_count = len(self._city_to_len[key])
            for elem in self._city_to_len[key]:
                sum_of_lens += elem
            x_coordinates.append(key)
            y_coordinates.append(int(sum_of_lens/posts_count))
        return x_coordinates, y_coordinates


    @staticmethod
    def _plot_graph(coordinates_tuple, **kwargs):
        x_coordinates, y_coordinates = coordinates_tuple
        plt.title(kwargs['name'])
        if type(x_coordinates[0]) == type(str()):
            plt.xticks(range(len(x_coordinates)), x_coordinates)
        else:
            plt.xlabel(kwargs['x_label'])
        plt.ylabel(kwargs['y_label'])
        plt.scatter(range(len(x_coordinates)), y_coordinates)
        plt.savefig('pic/'+kwargs['name']+'.pdf')
        pass

    @staticmethod
    def _get_coordinates_by_id(mapper):
        coordinates = []
        for key in mapper.keys():
            if mapper[key] is not None:
                coordinates.append(mapper[key])
        return coordinates

    def _get_post_len_to_comment_len(self):
        self.post_len_to_comment_len = {}
        for key in self.post_id_to_len:
            self.post_len_to_comment_len.setdefault(self.post_id_to_len[key], []).append(self.post_id_to_comments_len[key])

    def _get_post_to_len(self):
        self.post_id_to_len = {}
        for post in self.group_obj.posts:
            self.post_id_to_len[post.post_id] = self._get_len_of_text(post.text)

    def _get_post_to_comment_len(self):
        self.post_id_to_comments_len = {}
        for post in self.group_obj.posts:
            sum_comments_len = 0
            for comment in post.comments:
                sum_comments_len += self._get_len_of_text(comment.text)
            try:
                mean_comments_len = sum_comments_len / len(post.comments)
            except ZeroDivisionError:
                mean_comments_len = None
            self.post_id_to_comments_len[post.post_id] = mean_comments_len

if __name__ == '__main__':
    a = VkGroup(OWNER_ID)
    x = VkGroupStats(a)
    x.plot_city()
    x.plot_post_len_to_comments_len()
    x.plot_age()
