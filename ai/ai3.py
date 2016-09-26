import tensorflow as tf
import numpy as np
import os

if __name__ == '__main__':
	from util import Affine, ConvReluPool, TFModel
else:
	from ai.util import Affine, ConvReluPool, TFModel
# write your model
#def inference(x, dropout):
def inference(x):
	dropout = 0.75
	x_ = (x - 255.) / (-256.)
	d1, d2 = 64, 32 # 0.685
	# d1, d2 = 32, 16 # 0.67
	# d1, d2 = 64, 32 # 0.63
	# d1, d2 = 128, 64 # 0.60
	# d1, d2 = 64, 8 # 0.63
	# d1, d2 = 8, 8 # 0.68
	# d1, d2 = 4, 8 # 0.48
	# d1, d2 = 8, 4 # 0.58
	x1 = tf.nn.sigmoid(Affine(32*32, d1)(x_))
	x1_ = tf.nn.dropout(x1, dropout)
	x2 = tf.nn.sigmoid(Affine(d1, d2)(x1_))
	x3 = tf.nn.softmax(Affine(d2, 9)(x2))
	return x3
def loss(y, y_):
	y__ = tf.clip_by_value(y_,1e-10,1e10)
	return tf.reduce_mean(tf.reduce_sum(-y*tf.log(y__, ), reduction_indices=[1]))

def training(l):
	opt = tf.train.AdagradOptimizer(1e-1)
	# opt = tf.train.AdagradOptimizer(5e-2)
	# opt = tf.train.GradientDescentOptimizer(1e-1)
	return opt.minimize(l)

model = TFModel(inference, training, loss)
#model = TFModel(inference, training, loss, has_dropout=True)
if __name__ == '__main__':
	import reader
	batch_size = 50 # TODO
	#steps = 30000 #TODO
	steps = 100000 #TODO
	# steps = 200000 #TODO

	fname = "bin"
	data_set = reader.input_data(fname)
	save_file = "save/ai3.ckpt"
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		model.train(sess, steps, batch_size, data_set.train, data_set.test)
		#model.train(sess, steps, batch_size, data_set.train, data_set.test, dropout=0.75)
		model.save(sess, save_file)
		acc = model.accuracy(sess, data_set.test)
		print("test accuracy %g" % acc)

