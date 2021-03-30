import requests
from config import urlPrefix

class api:
    @staticmethod
    def send_msg(type, user, group, content):
        url = urlPrefix + 'send_msg'
        params = {}
        if type == 'private':
            params = {
                'message_type': type,
                'user_id': user,
                'message': content
            }
        else:
            params = {
                'message_type': type,
                'group_id': group,
                'message': content
            }
        requests.get(url, params = params)