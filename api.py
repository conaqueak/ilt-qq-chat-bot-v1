import requests
import json
import re
import time
from config import urlPrefix

class api:
    @staticmethod
    def grab(game):
        output = ''
        if game == 'ffxiv':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
            params = {
                'url': 'List?gameCode=ff',
                'category': '5309,5310,5311,5312,5313',
                'pageIndex': '1',
                'pageSize': '5',
                'callback': '_jsonpvvsnq69ejrl'
            }
            url = 'https://ff.web.sdo.com/inc/newdata.ashx'
            res = requests.get(url, params = params, headers = headers)
            data = res.text
            obj = re.compile(r'_json[0-9a-z]{12}\((?P<json>.*?)\)')
            content = obj.search(data).group('json')
            dic = json.loads(content)
            list = dic['Data']
            for each in list:
                title = each['Title']
                text = each['Summary']
                location = each['Author']
                image = each['HomeImagePath']
                publish = each['PublishDate']
                mix = f'[CQ:image,file={image}]\n标题：{title}\n内容：{text}\n发布时间：{publish}\n{location}\n-----\n'
                output += mix
        elif game == 'apex':
            params = {
                'auth': '4e023e657628f823c1fbb0d9f09e61e3',
                'lang': 'zh-TW'
            }
            url = 'https://api.mozambiquehe.re/news'
            res = requests.get(url, params = params)
            data = res.text
            dic = json.loads(data)
            for i in range(5):
                title = dic[i]['title']
                link = dic[i]['link']
                img = dic[i]['img']
                desc = dic[i]['short_desc']
                mix = f'[CQ:image,file={img}]\n标题：{title}\n内容：{desc}\n{link}\n-----\n'
                output += mix
        elif game == 'ow':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
            params = {
                'p': '1',
                'pageSize': '5'
            }
            url = 'https://ow.blizzard.cn/action/article/list'
            res = requests.get(url, params = params, headers = headers)
            data = res.text
            dic = json.loads(data)
            list = dic['data']['list']
            for i in range(5):
                title = list[i]['title']
                desc = list[i]['description']
                url = list[i]['linkUrl']
                if re.search('\/article\/news\/', url):
                    url = 'https://ow.blizzard.cn' + url
                publish = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(list[i]['publishTime']) / 1000))
                image = list[i]['thumbnailUrl']
                mix = f'[CQ:image,file={image}]\n标题：{title}\n内容：{desc}\n发布时间：{publish}\n{url}\n-----\n'
                output += mix
        return output

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

    @staticmethod
    def send_msg_news(group_id, game):
        url = urlPrefix + 'send_msg'
        content = api.grab(game)
        params = {
            'message_type': 'group',
            'group_id': group_id,
            'message': content
        }
        requests.get(url, params = params)