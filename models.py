from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask import jsonify

class Image(db.Model):
	__tablename__ = 'image'

	id = db.Column(db.Integer, primary_key=True)
	image = db.Column(db.LargeBinary(8192))
	label = db.Column(db.Integer)
	# dataは数値0~255の列
	def __init__(self, data, label):
		ar = [int(a) for a in data]
		ar = [a if 0 <= a < 256 else (0 if a < 0 else 255) for a in ar]
		self.image = bytes(ar)
		self.label = label
	def __repr__(self):
		return '<id {}>'.format(self.id)

	def bin(self):
		ar = bytearray(self.image)
		ar.append(self.label)
		return bytes(ar)

	def to_json(self):
		return jsonify({
			"image": list(self.image),
			"label": self.label
			})
	@classmethod
	def statistics(clz):
		res = []
		for i in range(1, 10):
			c = clz.query.filter(clz.label==i).count()
			res.append({
				"label": i,
				"count": c
				})
		return res
	@classmethod
	def clean(clz):
		clz.query.delete()


