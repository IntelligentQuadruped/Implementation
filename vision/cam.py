'''
Author: Viveque Ramji
Purpose: Module to connect to camera and retrieve rgb or depth data

'''

# import pyrealsense as pyrs
from skimage.transform import rescale
import numpy as np
import logging

class Camera:
	"""
    Object to get data from Realsense Camera
    """

	def __init__(self, frames=5, heightRatio=0.5, subSample=0.3, maxVal=4):
		"""
	    Intitalize Camera object with following optional parameters:
	    	frames			Number of frames to average over
	    	heightRatio 	Ratio of bottom part of image to keep
	    	subSample		Rescale image by subSample
	    	maxVal			Upper values to keep in depth image
	    """
		self.frames = frames
		self.heightRatio = heightRatio
		self.subSample = subSample
		self.maxVal = maxVal

	def connect(self):
		"""
	    Establish connection to R200 camera
	    """

		logging.info("Cam.py: Starts to connect components.")
		self.serv = pyrs.Service()
		self.dev = self.serv.Device(device_id=0, 
									streams=[pyrs.stream.DepthStream(fps=60),
											 pyrs.stream.ColorStream(fps=60)])


	def disconnect(self):
		"""
	    Disconnect from R200 camera
	    """

		self.dev.stop()
		self.serv.stop()
		logging.info("Cam.py: Camera Disconnected")

	def __reduce_frame(self, depth, h=0):
		"""
	    Takes in a depth image and removes 0 and values bigger than maxVal
	    Will also crop image to be last h rows
	    """
		if h:
			depth = depth[-h:-10, 69:-10]
		depth[depth <= 0] = np.nan
		depth[depth > self.maxVal] = np.nan

		return depth

	def get_frames_from_file(self, filename):
		"""
	    Function used for testing on saved files
	    Gets images from file, cleans and averages depth images and scales down
	    by subSample
	    """
		npz = np.load(filename)

		col = npz['arr_0']
		d = npz['arr_1']/1000
		h = int(self.heightRatio*(d.shape[0]))

		red = self.__reduce_frame(d, h)

		for i in range(self.frames-1):
			s = 'arr_%d' % (i+2)
			curr = self.__reduce_frame(npz[s]/1000, h)
			red = np.dstack((red, curr))

		meand = np.nanmean(red, 2)
		redmeand = self.__reduce_frame(meand)
		final = rescale(redmeand, self.subSample)

		return final, col


	def get_frames(self, rgb=False):
		"""
	    Function will retrieve depth frames (and rgb if true) from R200 input
	    Cleans and averages depth images and scales down by subSample
	    """
		self.dev.wait_for_frames()
		if rgb:
			col = self.dev.color 

		d = self.dev.depth * self.dev.depth_scale
		h = int(self.height_ratio*(d.shape[0]))

		red = self.__reduce_frame(d, h)

		for i in range(self.frames-1):
			self.dev.wait_for_frames()
			curr = self.__reduce_frame(self.dev.depth*self.dev.depth_scale, h)
			red = np.dstack((red, curr))

		meand = np.nanmean(red, 2)
		redmeand = self.__reduce_frame(meand)
		final = rescale(redmeand, self.subSample)

		return final, col



			





