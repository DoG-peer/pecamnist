import numpy as np

class Reader():
	def __init__(self, fname):
		self.fname = fname
	def read_all(self):
		unit = 32*32+1
		images = []
		labels = []
		with open(self.fname, "rb") as f:
			while True:
				x = f.read(unit)
				if(len(x) == 0):
					break
				label = x[unit-1]
				labels.append(label)
				image = x[:unit-1]
				images.append(image)
		return images, labels

class DataSet():
	def __init__(self, imgs, labels):
		self.length = len(labels)
		self.images = np.array([list(img) for img in imgs], dtype=np.float)
		self.labels = np.zeros([self.length, 9], dtype=np.float)
		for i, label in enumerate(labels):
			if type(label) == int:
				self.labels[i, label-1] = 1.0
			else:
				self.labels[i] = label
		self.pos = 0
		self.shuffled_ids = list(range(self.length))
		np.random.shuffle(self.shuffled_ids)

	# 高々n個取る
	def next_batch(self, n):
		if self.pos + n >= self.length:
			np.random.shuffle(self.shuffled_ids)
			self.pos = 0
		pos0 = self.pos
		pos1 = self.pos + n

		imgs = [self.images[i] for i in self.shuffled_ids[pos0:pos1]]
		labels = [self.labels[i] for i in self.shuffled_ids[pos0:pos1]]

		self.pos = pos1
		return imgs, labels
	def split(self, p):
		n0 = int(self.length*p)
		np.random.shuffle(self.shuffled_ids)
		imgs0 = [self.images[i] for i in self.shuffled_ids[:n0]]
		labels0 = [self.labels[i] for i in self.shuffled_ids[:n0]]
		imgs1 = [self.images[i] for i in self.shuffled_ids[n0:]]
		labels1 = [self.labels[i] for i in self.shuffled_ids[n0:]]
		return DataSet(imgs0, labels0), DataSet(imgs1, labels1)

	@classmethod
	def load(clz, fname):
		imgs, labels = Reader(fname).read_all()
		return clz(imgs, labels)

class SplittedData():
	def __init__(self, train, test):
		self.train = train
		self.test  = test
	# 高々n個取る
	def next_batch(self, n):
		return self.train.next_batch(n)
def input_data(fname):
	total_data = DataSet.load(fname)
	train, test = total_data.split(0.8)
	return SplittedData(train, test)

if __name__ == '__main__':
	fname = "/home/user/projects/pecamnist/ai/bin"
	x = DataSet("bin")
	imgs, labels = x.next_batch(10)
	print(imgs)
	print(labels)


