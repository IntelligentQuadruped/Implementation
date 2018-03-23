'''
Author: Viveque Ramji
Purpose: Module to connect to camera and retrieve rgb or depth data

'''

# import pyrealsense as pyrs
from skimage.transform import rescale
import numpy as np

class Camera:

	def __init__(self, frames=5, height_ratio=0.5, subSample=0.3, maxval=4):
		self.frames = frames
		self.height_ratio = height_ratio
		self.subSample = subSample
		self.maxval = maxval

	def connect(self):
		self.ser = pyrs.Service()
		self.dev = serv.Device(device_id=0, streams=[pyrs.stream.DepthStream(fps=60), 
    						   pyrs.stream.ColorStream(fps=60)])

	def disconnect(self):
		self.dev.stop()
		self.serv.stop()

	def __reduce_frame(self, depth, h=0):

		if h:
			depth = depth[-h:,:]
		depth[depth <= 0] = np.nan
		depth[depth > self.maxval] = np.nan

		return depth

	def get_frames_from_file(self, filename):
		npz = np.load(filename)

		col = npz['arr_0']
		d = npz['arr_1']/1000
		h = int(self.height_ratio*(d.shape[0]))

		d = self.__reduce_frame(d, h)

		for i in range(self.frames-1):
			s = 'arr_%d' % (i+2)
			curr = self.__reduce_frame(npz[s]/1000, h)
			d = np.dstack((d, curr))

		d = np.nanmean(d, 2)
		d = self.__reduce_frame(d)
		d = rescale(d, self.subSample)

		return d, col


	def get_frames(self, rgb=False):
		self.dev.wait_for_frames()
		if rgb:
			col = self.dev.color 

		d = self.dev.depth * self.dev.depth_scale
		h = int(self.height_ratio*(d.shape[0]))

		d = self.__reduce_frame(d, h)

		for i in range(self.frames-1):
			self.dev.wait_for_frames()
			curr = self.__reduce_frame(self.dev.depth * self.dev.depth_scale, h)
			d = np.dstack((d, curr))

		d = np.nanmean(d, 2)
		d = self.__reduce_frame(d)
		d = rescale(d, self.subSample)

		return d, col



			




