from flask import request
from api import api

def register_routes(app):
	@app.route('/', methods=['POST'])
	def post_data():
		data = request.get_json()
		if data['post_type'] == 'meta_event':
			return 'OK'
		if data['message'] == '/help':
			content = f'[CQ:at,qq={data["user_id"]}]\n/ffxiv news：查看关于最终幻想14的新闻\n/apex news：查看关于Apex英雄的新闻\n/apex player [Origin ID]：查询Apex英雄的玩家信息\n/apex map：查询Apex英雄当前的地图轮换\n/apex predator：查询Apex英雄当前的猎杀者分数线与大师人数\n/ow news：查看关于守望先锋的新闻'
			api.send_msg(data['message_type'], data['user_id'], data['group_id'], content)
		elif data['message'] == '/ffxiv news':
			api.send_msg_news(data['group_id'], 'ffxiv')
		return 'OK'