from flask import request

def register_routes(app):
	@app.route('/', methods=['POST'])
	def post_data():
		data = request.get_json()
		if data['post_type'] == 'meta_event':
			return 'OK'
		return 'OK'