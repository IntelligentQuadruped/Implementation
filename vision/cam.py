'''
Author: Viveque Ramji
Purpose: Module to connect to camera and retrieve rgb or depth data

'''

# import pyrealsense as pyrs
from skimage.transform import rescale
import numpy as np
import logging
import time

import matplotlib.pyplot as plt

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
		h = int(self.height_ratio*(d.shape[0]))

		d = d[-h:-30, 69:-10]
		d[d <= 0] = np.nan
		d[d > 4] = np.nan

		final = rescale(d, self.sub_sample)

		return final


	def getFramesFromFile(self, filename, idx):
		"""
	    Function used for testing on saved files
	    Gets images from file, cleans and averages depth images and scales down
	    by sub_sample
	    """

		colf = filename + 'c.npy'
		df = filename + 'd.npy'
		col = np.load(colf % idx)
		d = np.load(df % idx)/1000.

		for i in range(self.frames-1):
			idy = idx+i+1
			s = np.load(df % idy)/1000.
			d = np.dstack((d, s))

		meand = np.nanmean(d, 2)
		meand[meand > 4] = np.nan

		return meand, col


	def getFrames(self, rgb=False):
		"""
	    Function will retrieve depth frames (and rgb if true) from R200 input
	    Cleans and averages depth images and scales down by sub_sample
	    """
		self.dev.wait_for_frames()
		if rgb:
			col = self.dev.color 

		d = self.dev.depth * self.dev.depth_scale
		h = int(self.height_ratio*(d.shape[0]))

		red = self.__reduceFrame(d, h)

		for _ in range(self.frames-1):
			self.dev.wait_for_frames()
			curr = self.__reduceFrame(self.dev.depth*self.dev.depth_scale, h)
			red = np.dstack((red, curr))

		meand = np.nanmean(red, 2)
		red_meand = self.__reduceFrame(meand)
		final = rescale(red_meand, self.sub_sample)

		return final, col



			





