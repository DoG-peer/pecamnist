import tensorflow as tf
import numpy as np
import os
if __name__ == '__main__':
	from util import Affine, ConvReluPool, TFModel
else:
	from ai.util import Affine, ConvReluPool, TFModel
# write your model
def inference(x):
	h = Affine(32*32, 9)((x - 255.)/(-256.))
	return tf.nn.softmax(h)
def loss(y, y_):
	y__ = tf.clip_by_value(y_,1e-10,1e10)
	return tf.reduce_mean(tf.reduce_sum(-y*tf.log(y__), reduction_indices=[1]))

def training(l):
	opt = tf.train.AdagradOptimizer(1e-1)
	# opt = tf.train.GradientDescentOptimizer(1e-4)
	return opt.minimize(l)

model = TFModel(inference, training, loss)

if __name__ == '__main__':
	import reader
	batch_size = 50 # TODO
	steps = 15000 #TODO

	fname = "bin"
	data_set = reader.input_data(fname)
	save_file = "save/ai2.ckpt"
	with tf.Session() as sess:
		sess.run(tf.initialize_all_variables())
		model.train(sess, steps, batch_size, data_set.train, data_set.test)
		model.save(sess, save_file)
		acc = model.accuracy(sess, data_set.test)
		print("test accuracy %g" % acc)

