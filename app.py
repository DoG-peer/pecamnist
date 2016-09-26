from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import json
import random
app = Flask(__name__)

if 'APP_SETTINGS' in os.environ:
	app_settings = os.environ['APP_SETTINGS']
else:
	app_settings = "config.LearnedStagingConfig"
app.config.from_object(app_settings)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
learned = app.config["LEARNED"]

from models import Image
"""
top page
データを投稿できる

"""
@app.route('/')
@app.route('/index.html')
def index():
	return render_template('index.html', learned=learned)

@app.route('/help')
@app.route('/help.html')
def help():
	return render_template('help.html', learned=learned)

@app.route('/view/<int:key>')
@app.route('/view/<int:key>.html')
def view(key):
	return render_template('view.html',key=key, learned=learned)

@app.route('/api/view')
def view_api():
	n = Image.query.count()
	k = random.randint(0, n-1)
	img = Image.query.get_or_404(k)
	return img.to_json()

@app.route('/inference')
@app.route('/inference.html')
def inferpage():
	if learned:
		return render_template('inference.html', learned=learned)
	else:
		return render_template('not_learned.html', learned=learned)


@app.route('/statistics')
@app.route('/statistics.html')
def statistics():
	n = Image.query.count()
	print(Image.statistics())
	return render_template('statistics.html', n=n, learned=learned)

"""
@app.route('/api/items', methods=['GET'])
def get_all():
	return "all"
"""

@app.route('/api/items/<int:key>', methods=['GET'])
def get_item(key):
	item = Image.query.get_or_404(key)
	return item.to_json()


"""
base64で変換されたバイナリデータを受け取ってやり取りする？？
"""
@app.route('/api/items', methods=['POST'])
def new():
	data = json.loads(request.data.decode("utf-8"))
	# print(data)
	mnist = Image(data["image"], data["label"])
	db.session.add(mnist)
	db.session.commit()
	a = Image.query.first()
	return jsonify({});

if learned:
	import ai
	@app.route('/api/ai/infer', methods=['POST'])
	def infer():
		# データは{"ai_name": AIの名前, image: 長さ32*32の値0~255の配列}
		data = json.loads(request.data.decode("utf-8"))
		ai_name = data["ai_name"]
		image = data["image"]
		result = ai.infer(ai_name, image)
		result = [float(a) for a in result]
		return jsonify({"data": result})

"""
32*32+1バイト
32*32: データ
1: ラベル
"""
@app.route('/bin', methods=['GET'])
def bin():
	return b''.join([img.bin() for img in Image.query.all()])

if __name__ == '__main__':
	app.run(use_reloader=True)
