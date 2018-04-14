'''
Author: Viveque Ramji
Purpose: Module to connect to camera and retrieve rgb or depth data.
		 Currently supporting the R200 Intel Camera.

'''

import numpy as np
import logging
import time
import matplotlib.pyplot as plt
from skimage.transform import rescale

try:
	import pyrealsense as pyrs
except ImportError as error:
	print("Could not import pyrealsense")
	logging.warning("cam.py: WARNING: " + str(error))



class Camera:
	"""
    Object to get data from Realsense Camera
    """
	def __init__(self, frames=5, height_ratio=0.5, sub_sample=0.3, max_val=4):
		"""
	    Intitalize Camera object with following optional parameters:
	    	frames			Number of frames to average over
	    	height_ratio 	Ratio of bottom part of image to keep
	    	sub_sample		Rescale image by sub_sample
	    	max_val			Upper values to keep in depth image
	    """

		self.frames = frames
		self.height_ratio = height_ratio
		self.sub_sample = sub_sample
		self.max_val = max_val

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

	def reduceFrame(self, depth):
		"""
	    Takes in a depth image and removes 0 and values bigger than max_val
	    Will also crop image to be last h rows
	    """
		d = depth.copy()
		height = d.shape[0]
		h = int(self.height_ratio*(height))

		up = height/2 + h/2
		low = height/2 - h/2

		d = d[h:, 10:-10]
		d[d <= 0] = np.nan
		d[d > 4] = np.nan

		final = rescale(d, self.sub_sample)

		return final

	def getFrames(self, rgb=False):
		"""
	    Function will retrieve depth frames (and rgb if true) from R200 input
	    Cleans and averages depth images and scales down by sub_sample
	    """
		self.dev.wait_for_frames()

		d = self.dev.depth*self.dev.depth_scale

		for _ in range(self.frames-1):
			self.dev.wait_for_frames()
			curr = self.dev.depth*self.dev.depth_scale
			d = np.dstack((d, curr))

		if self.frames != 1:
			d = np.nanmean(d, 2)
		d[d > 4] = np.nan

		if rgb:
			col = self.dev.color 
			return d, col

		return d

	def getFramesFromFile(self, filename, idx=None):
		"""
		Function used for testing on saved files
		Gets images from file, cleans and averages depth images and scales down
		by sub_sample
		"""
		if idx is None:
			string = filename.replace("_"," ")
			numbers = [int(s) for s in str.split(string) if s.isdigit()]
			idx = numbers[-1]
			print(idx)

		colf = filename + 'c.npy'
		df = filename + 'd.npy'
		col = np.load(colf)
		d = np.load(df)/1000.
		colf = colf.replace(str(idx),'%d')
		df = df.replace(str(idx),'%d')

		for i in range(self.frames-1):
			idy = idx+i+1
			s = np.load(df % idy)/1000.
			d = np.dstack((d, s))

		if self.frames != 1:
			d = np.nanmean(d, 2)
		d[d > 4] = np.nan

		return d, col






