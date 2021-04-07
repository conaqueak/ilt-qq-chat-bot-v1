import requests
import json
import re
import time
from config import urlPrefix
from utils import transToChinese, endTime, timeRemain

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

    @staticmethod
    def send_msg_apex_player(user_id, group_id, name):
        params = {
            'auth': '4e023e657628f823c1fbb0d9f09e61e3',
            'player': name,
            'platform': 'PC',
            'enableClubsBeta': 'true'
        }
        url = 'https://api.mozambiquehe.re/bridge'
        res = requests.get(url, params = params)
        content = res.text
        dic = json.loads(content)
        ban = None
        if dic["global"]["bans"]["isActive"] == False:
            ban = '否'
        else:
            ban = '是'
        rank = None
        rankScore = dic["global"]["rank"]["rankScore"]
        rankDiv = str(dic["global"]["rank"]["rankDiv"])
        brLadderPos = dic["global"]["rank"]["ladderPosPlatform"]
        if dic["global"]["rank"]["rankName"] == 'Unranked':
            rank = '未定级'
        elif dic["global"]["rank"]["rankName"] == 'Rookie':
            rank = '菜鸟' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Bronze':
            rank = '青铜' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Silver':
            rank = '白银' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Gold':
            rank = '黄金' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Platinum':
            rank = '白金' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Diamond':
            rank = '钻石' + rankDiv + f'（{rankScore}分）'
        elif dic["global"]["rank"]["rankName"] == 'Master':
            rank = '大师' + f'（{rankScore}）'
        elif dic["global"]["rank"]["rankName"] == 'Apex Predator':
            rank = '猎杀者' + f'#{brLadderPos}' + f'（{rankScore}分）'
        arena = None
        arenaScore = dic["global"]["arena"]["rankScore"]
        arenaDiv = str(dic["global"]["arena"]["rankDiv"])
        aLadderPos = dic["global"]["arena"]["ladderPosPlatform"]
        if dic["global"]["arena"]["rankName"] == 'Unranked':
            arena = '未定级'
        elif dic["global"]["arena"]["rankName"] == 'Rookie':
            arena = '菜鸟' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Bronze':
            arena = '青铜' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Silver':
            arena = '白银' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Gold':
            arena = '黄金' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Platinum':
            arena = '白金' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Diamond':
            arena = '钻石' + arenaDiv + f'（{arenaScore}分）'
        elif dic["global"]["arena"]["rankName"] == 'Master':
            arena = '大师' + f'（{arenaScore}）'
        elif dic["global"]["arena"]["rankName"] == 'Apex Predator':
            arena = '猎杀者' + f'#{aLadderPos}' + f'（{arenaScore}分）'
        lobbyState = dic["realtime"]["lobbyState"]
        if lobbyState == 'open':
            lobbyState = '公开'
        isOnline = dic["realtime"]["isOnline"]
        if isOnline:
            isOnline = '在线'
        else:
            isOnline = '离线'
        isInGame = dic["realtime"]["isInGame"]
        if isInGame:
            isInGame = '正在游戏中'
        else:
            isInGame = '大厅待机中'
        canJoin = dic["realtime"]["canJoin"]
        if canJoin:
            canJoin = '可加入'
        else:
            canJoin = '不可加入'
        partyFull = dic["realtime"]["partyFull"]
        if partyFull:
            partyFull = '满编小队'
        else:
            partyFull = '轻锐小队'
        currentTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        content = f'[CQ:at,qq={user_id}]\n查询时间：{currentTime}\n玩家名称：{dic["global"]["name"]}\n当前状态：{isOnline}（{isInGame}）\n当前等级：{dic["global"]["level"]}\n当前经验：{dic["global"]["toNextLevelPercent"]}%\n禁赛状态：{ban}\n大逃杀段位：{rank}\n竞技场段位：{arena}\n组队状态：{lobbyState}{partyFull}（{canJoin}）\n'
        club = dic['club']['id']
        if club != None:
            content = f'[CQ:image,file={dic["club"]["logo"]}]\n' + content + f'俱乐部：[{dic["club"]["tag"]}] {dic["club"]["name"]}（{dic["club"]["groupSize"]}/{dic["club"]["maxGroupSize"]}）'
        params = {
            'message_type': 'group',
            'group_id': group_id,
            'message': content
        }
        url = urlPrefix + 'send_msg'
        requests.get(url, params = params)

    @staticmethod
    def send_msg_apex_map(user_id, group_id):
        params = {
            'auth': '4e023e657628f823c1fbb0d9f09e61e3',
            'version': '2'
        }
        url = 'https://api.mozambiquehe.re/maprotation'
        res = requests.get(url, params = params)
        content = res.text
        dic = json.loads(content)
        brCurrent = dic["battle_royale"]["current"]["map"]
        brCurrent = transToChinese(brCurrent)
        brEndTime = endTime(dic["battle_royale"]["current"]["end"])
        brTimeRemain = timeRemain(dic["battle_royale"]["current"]["remainingSecs"])
        brNext = dic["battle_royale"]["next"]["map"]
        brNext = transToChinese(brNext)
        brNextDuration = timeRemain(dic["battle_royale"]["next"]["DurationInSecs"])

        brRankCurrent = dic["ranked"]["current"]["map"]
        brRankCurrent = transToChinese(brRankCurrent)
        brRankEndTime = endTime(dic["ranked"]["current"]["end"])
        brRankTimeRemain = timeRemain(dic["ranked"]["current"]["remainingSecs"])
        brRankNext = dic["ranked"]["next"]["map"]
        brRankNext = transToChinese(brRankNext)
        brRankNextDuration = timeRemain(dic["ranked"]["next"]["DurationInSecs"])

        aCurrent = dic["arenas"]["current"]["map"]
        aCurrent = transToChinese(aCurrent)
        aEndTime = endTime(dic["arenas"]["current"]["end"])
        aTimeRemain = timeRemain(dic["arenas"]["current"]["remainingSecs"])
        aNext = dic["arenas"]["next"]["map"]
        aNext = transToChinese(aNext)
        aNextDuration = timeRemain(dic["arenas"]["next"]["DurationInSecs"])

        aRankCurrent = dic["arenasRanked"]["current"]["map"]
        aRankCurrent = transToChinese(aRankCurrent)
        aRankEndTime = endTime(dic["arenasRanked"]["current"]["end"])
        aRankTimeRemain = timeRemain(dic["arenasRanked"]["current"]["remainingSecs"])
        aRankNext = dic["arenasRanked"]["next"]["map"]
        aRankNext = transToChinese(aRankNext)
        aRankNextDuration = timeRemain(dic["arenasRanked"]["next"]["DurationInSecs"])

        currentTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        content = f'[CQ:at,qq={user_id}]\n查询时间：{currentTime}\n>【大逃杀丨匹配模式】\n当前地图：{brCurrent}\n结束时间：{brEndTime}\n剩余时间：{brTimeRemain}\n即将轮换：{brNext}\n持续时间：{brNextDuration}\n>【大逃杀丨排位模式】\n当前地图：{brRankCurrent}\n结束时间：{brRankEndTime}\n剩余时间：{brRankTimeRemain}\n即将轮换：{brRankNext}\n持续时间：{brRankNextDuration}\n>【竞技场丨匹配模式】\n当前地图：{aCurrent}\n结束时间：{aEndTime}\n剩余时间：{aTimeRemain}\n即将轮换：{aNext}\n持续时间：{aNextDuration}\n>【竞技场丨排位模式】\n当前地图：{aRankCurrent}\n结束时间：{aRankEndTime}\n剩余时间：{aRankTimeRemain}\n即将轮换：{aRankNext}\n持续时间：{aRankNextDuration}'
        params = {
            'message_type': 'group',
            'group_id': group_id,
            'message': content
        }
        url = urlPrefix + 'send_msg'
        requests.get(url, params = params)

    @staticmethod
    def send_msg_apex_predator(user_id, group_id):
        params = {
            'auth': '4e023e657628f823c1fbb0d9f09e61e3'
        }
        url = 'https://api.mozambiquehe.re/predator'
        res = requests.get(url, params = params)
        content = res.text
        dic = json.loads(content)
        totalBRMaster = dic["RP"]["PC"]["totalMastersAndPreds"]
        if totalBRMaster > 750:
            totalBRMaster -= 750
        totalAMaster = dic["AP"]["PC"]["totalMastersAndPreds"]
        if totalAMaster > 750:
            totalAMaster -= 750
        currentTime = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        content = f'[CQ:at,qq={user_id}]\n>【大逃杀模式】\n猎杀者分数线：{dic["RP"]["PC"]["val"]}\n大师总人数：{totalBRMaster}\n>【竞技场模式】\n猎杀者分数线：{dic["AP"]["PC"]["val"]}\n大师总人数：{totalAMaster}'
        params = {
            'message_type': 'group',
            'group_id': group_id,
            'message': content
        }
        url = urlPrefix + 'send_msg'
        requests.get(url, params = params)

    @staticmethod
    def get_compare_send():
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
        i = 0
        oldId = list[i]['Id']
        while True:
            res = requests.get(url, params = params, headers = headers)
            data = res.text
            obj = re.compile(r'_json[0-9a-z]{12}\((?P<json>.*?)\)')
            content = obj.search(data).group('json')
            dic = json.loads(content)
            list = dic['Data']
            id = list[i]['Id']
            time.sleep(5)
            if oldId == id:
                i = 0
                oldId = list[i]['Id']
                print('未检测到新内容')
                continue
            id = list[i]['Id']
            title = list[i]['Title']
            text = list[i]['Summary']
            location = list[i]['Author']
            image = list[i]['HomeImagePath']
            publish = list[i]['PublishDate']
            mix = f'[CQ:image,file={image}]\n标题：{title}\n内容：{text}\n发布时间：{publish}\n{location}'
            api.send_msg('group', '21296949', '600082002', mix)
            print('检测到新的公告！')
            print(mix)
            i += 1