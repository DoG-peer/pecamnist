import tensorflow as tf
import numpy as np

class Affine():
	def __init__(self, d_in, d_out):
		with tf.variable_scope("Affine", reuse=False):
			self.w = tf.Variable(tf.random_normal([d_in, d_out]), dtype=tf.float32)
			self.b = tf.Variable(tf.random_normal([d_out]), dtype=tf.float32)

	def __call__(self, x):
		return tf.matmul(x, self.w) + self.b

class ConvReluPool():
	# wは4階のテンソル
	# bはベクトル
	def __init__(self, wc, bc):
		with tf.variable_scope("ConvReluPool", reuse=False):
			self.w = tf.Variable(tf.random_normal(wc), dtype=tf.float32)
			self.b = tf.Variable(tf.random_normal(bc), dtype=tf.float32)
	def __call__(self, x):
		c = tf.nn.conv2d(x, self.w, strides=[1,1,1,1], padding='SAME')
		l = tf.nn.relu(c)
		return tf.nn.max_pool(l, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME') + self.b

class TFModel():
	def __init__(self, inference, training, loss, has_dropout=False):
		x = tf.placeholder(tf.float32, [None, 32*32])
		y = tf.placeholder(tf.float32, [None, 9])

		if has_dropout:
			self.dropout = tf.placeholder_with_default(1.0, [])
			y_ = inference(x, self.dropout)
		else:
			y_ = inference(x)

		loss_val = loss(y, y_)
		train = training(loss_val)
		correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
		accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		self.x = x
		self.y = y
		self.y_ = y_
		self.has_dropout = has_dropout
		self.train_task = train
		self.accu = accuracy
		self.saver = tf.train.Saver()

	def train(self, sess, steps, batch_size, data_set, test_data_set=None, dropout=None):
		for i in range(steps):
			batch_xs, batch_ys = data_set.next_batch(batch_size)
			if dropout != None and self.has_dropout:
				sess.run(self.train_task, {self.x: batch_xs, self.y: batch_ys,
					self.dropout: dropout})
			else:
				sess.run(self.train_task, {self.x: batch_xs, self.y: batch_ys})
			if (i+1) % 100 == 0:
				train_acc = sess.run(self.accu, {self.x: batch_xs, self.y: batch_ys})
				print("step %d, train accuracy %g" % (i+1, train_acc))
				if (i+1) % 1000 == 0 and test_data_set != None:
					test_acc = sess.run(self.accu, {
						self.x: test_data_set.images,
						self.y: test_data_set.labels})
					print("\t\ttest accuracy %g" % test_acc)
	def save(self, sess, fname):
		self.saver.save(sess, fname)

	def restore(self, sess, fname):
		self.saver.restore(sess, fname)

	def accuracy(self, sess, data_set):
		return sess.run(self.accu, {self.x: data_set.images, self.y: data_set.labels})

	def serve(self, fname):
		self.sess = tf.Session()
		self.restore(self.sess, fname)
		return self.sess

	def infer(self, data, sess=None):
		if sess==None:
			sess = self.sess
		xs = np.array([data], dtype=np.float32)
		return sess.run(self.y_, {self.x: xs})[0]



