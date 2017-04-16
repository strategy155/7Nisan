import requests
import json
import datetime


def get_post_ids(owner_id=-104603396):
    all_posts = {}
    i = 0
    while True:
        req_obj = requests.get('https://api.vk.com/method/wall.get?owner_id='+str(owner_id)+'&count=100&offset='+str(i))
        resp_arr = json.loads(req_obj.text)['response']
        leng = len(resp_arr)
        for elem in resp_arr:
            if type(elem) == type(dict()):
                date = datetime.datetime.fromtimestamp(
                        int(resp_arr[1]['date'])
                        ).strftime('%Y-%m')

                try:
                    all_posts[date].append(elem['id'])
                except KeyError:
                    all_posts[date] = [elem['id']]
        if leng == 1:
            break
        if i >=300:
            break
        i +=100
    return all_posts


def count_comments(post_id, owner_id=-104603396):
    req_obj = requests.get('https://api.vk.com/method/wall.getComments?owner_id='+str(owner_id)+'&post_id='+str(post_id))
    resp_arr = json.loads(req_obj.text)['response']
    comms_count = resp_arr[0]
    return comms_count
