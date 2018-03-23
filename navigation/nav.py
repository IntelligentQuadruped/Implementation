'''
Author: Viveque Ramji
Purpose: Module to clean camera data and provide an open direction to move in

'''

'''
***************************************************************************************/
*	 __createSamples() and __reconstructDepthImage() adapted from:
*
*    Title: Sparse Depth Sensing for Resource-Constrained Robots
*    Author: Ma, Fangchang and Carlone, Luca and Ayaz, Ulas and Karaman, Sertac
*    Journal: arXiv preprint arXiv:1703.01398
*    Year: 2017
*    Availability: https://github.com/sparse-depth-sensing/sparse-depth-sensing
*
***************************************************************************************/
'''

import numpy as np
from scipy import sparse
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt


class Navigation:

	class __Data:
		def __init__(self, row_i, start_i, end_i, n):
			self.row_i = row_i
			self.start_i = start_i
			self.end_i = end_i
			self.n = n
			self.gap = None

		def compare_gap(self, s, f):
			g = self.gap
			if g != None:
				return g[1]-g[0] < f-s
			else:
				return True

		def get_gap(self):
			return self.gap

		def set_gap(self, s, f):
			g = self.gap
			if g == None:
				self.gap = (s, f)
			else:
				if f-s > g[1]-g[0]:
					self.gap = (s, f)



	def __init__(self, percSamples=0.1, angle_swept=60):

		self.percSamples = percSamples
		self.angle_swept = angle_swept

	def __createSamples(self, depth):
		height = depth.shape[0]
		width = depth.shape[1]
		N = height * width
		K = int(N * self.percSamples)

		xGT = depth.flatten()
		rand = np.random.permutation(N)[:K]
		a = np.isnan(xGT[rand])
		samples = rand[np.nonzero(~a)[0]]

		Rfull = sparse.eye(N)
		R = Rfull.tocsr()[samples,:]
		measured_vector = R*xGT

		return samples, measured_vector

	def __reconstructDepthImage(self, shape, measured_vector, samples):
		h = np.arange(0, shape[0])
		w = np.arange(0, shape[1])

		Yq, Zq = np.meshgrid(w, h)
		Y_sample = Yq.flatten()[samples]
		Z_sample = Zq.flatten()[samples]

		rbf1 = Rbf(Y_sample, Z_sample, measured_vector, function='linear')
		RBF1 = rbf1(Yq, Zq)

		return RBF1

	def __find_largest_gap(self, depth, max_dist):
		depth =  depth > max_dist # true where gap exists
		npad = ((0, 0), (1, 1))
		d = np.pad(depth, pad_width=npad, mode='constant', constant_values=0)

		f = np.nonzero(np.diff(d))
		r = f[0][0::2] # row indices
		data = self.__Data(r, f[1][0::2], f[1][1::2], len(np.unique(r)))

		self.__add_next_row(0, 0, np.inf, data)

		sf = data.get_gap()
		if sf == None:
			return None

		return (sf[0]+sf[1])/2

	def __add_next_row(self, row, start, finish, data):
		if row == data.n:
			data.set_gap(start, finish)
			return
		args = np.argwhere(data.row_i == row)
		for i in args:
			s = start
			f = finish
			c = data.start_i[i][0]
			d = data.end_i[i][0]
			if s < d and f > c:
				if s < c:
					s = c
				if f > d:
					f = d
				if data.compare_gap(s, f):
					self.__add_next_row(row+1, s, f, data)
			return


	def reconstruct_frame(self, depth):
		samples, measured_vector = self.__createSamples(depth)
		return self.__reconstructDepthImage(depth.shape, measured_vector, samples)

	def obstacle_avoid(self, depth, max_dist):
	  	pos = self.__find_largest_gap(depth, max_dist)
	  	if pos is None:
	  		return(None, None)
	  	
	  	deg = 1.*self.angle_swept*pos/depth.shape[1] - self.angle_swept/2.
	  	frac = 2.*pos/depth.shape[1] - 1
	  	return (frac, deg)

	def plot(self, rgb, depth, interpolated, pos, cmap='gray'):
		plt.subplot(2, 2, 1)
		plt.title('RGB')
		plt.imshow(rgb)
		plt.scatter(pos, 460)
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 2)
		plt.imshow(depth, cmap=cmap)
		plt.title('Original')
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 3)
		plt.imshow(interpolated, cmap=cmap)
		plt.title('rbf1')
		plt.xticks(visible=False)
		plt.yticks(visible=False)


		plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
		cax = plt.axes([0.85, 0.1, 0.075, 0.8])
		plt.colorbar(cax=cax)

		plt.show()



	  


















