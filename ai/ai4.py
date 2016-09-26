import tensorflow as tf
import numpy as np
import os

if __name__ == '__main__':
	from util import Affine, ConvReluPool, TFModel
else:
	from ai.util import Affine, ConvReluPool, TFModel
# x [None, 32*32]
# x_ [None, 32, 32, 1]
# | <= conv(W: [5, 5, 1, 32])
# | <= relu
# | <= pool
# | + b: [32]
# h1 [None, 16, 16, 32]
# | <= conv(W: [5, 5, 32, 64])
# | <= relu
# | <= pool
# | + b: [64]
# h2 [None, 8, 8, 64]
# h2_ [None, 8*8*64]
# | <= Affine(W: [8*8*64, 1024], b: [1024]) <= is b nesseary?
# | <= relu
# hfc [None, 1024]
#%% | <= dropout
#%% hfc_drop [None, 1024]
# | <= Affine(W: [1024, 9], b: [9])
# | <= softmax
# y [None, 9]

# write your model
def inference(x):
	x = (x-255.)/(-256.)
	# d1, d2, d3 = 32, 64, 1024
	d1, d2, d3 = 16, 32, 256
	x_ = tf.reshape(x, [-1, 32, 32, 1])
	h1 = ConvReluPool([3, 3, 1, d1], [d1])(x_)
	h2 = ConvReluPool([3, 3, d1, d2], [d2])(h1)
	h2_ = tf.reshape(h2, [-1, 8*8*d2])
	hfc = tf.nn.sigmoid(Affine(8*8*d2, d3)(h2_))
	# hfc = tf.nn.relu(Affine(8*8*d2, 1024)(h2_))
	# hfc_drop = tf.dropout()
	return tf.nn.softmax(Affine(d3, 9)(hfc))
def loss(y, y_):
	y__ = tf.clip_by_value(y_,1e-10,1e10)
	return tf.reduce_mean(tf.reduce_sum(-y*tf.log(y__), reduction_indices=[1]))

def training(l):
	opt = tf.train.AdagradOptimizer(1e-1)
	return opt.minimize(l)

model = TFModel(inference, training, loss)
if __name__ == '__main__':
	import reader
	batch_size = 50 # TODO
	steps = 100000 #TODO
	fname = "bin"
	data_set = reader.input_data(fname)
	save_file = "save/ai4.ckpt"
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		model.train(sess, steps, batch_size, data_set.train, data_set.test)
		model.save(sess, save_file)
		acc = model.accuracy(sess, data_set.test)
		print("test accuracy %g" % acc)

