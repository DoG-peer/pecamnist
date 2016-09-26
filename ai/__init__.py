import tensorflow as tf

with tf.Graph().as_default():
	from ai.ai2 import model as ai2model
	ai2model.serve("ai/save/ai2.ckpt")
with tf.Graph().as_default():
	from ai.ai3 import model as ai3model
	ai3model.serve("ai/save/ai3.ckpt")
with tf.Graph().as_default():
	from ai.ai4 import model as ai4model
	ai4model.serve("ai/save/ai4.ckpt")

def infer(ai_name, image):
	if ai_name == "Softmax Regression":
		return ai2model.infer(image)
	elif ai_name == "多層パーセプトロン":
		return ai3model.infer(image)
	elif ai_name == "CNN":
		return ai4model.infer(image)
	else:
		return [0.1111] * 9

