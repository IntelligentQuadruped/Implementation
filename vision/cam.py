'''
Author: Viveque Ramji, Jan Bernhard
Purpose: Module to connect to camera and retrieve rgb or depth data.
		 Currently supporting the R200 Intel Camera.

'''

import numpy as np
import logging
import time
import matplotlib.pyplot as plt
from skimage.transform import rescale
from fileSupport import ensureDir
from os import path, makedirs

try:
	import pyrealsense as pyrs
except ImportError as error:
	print("Could not import pyrealsense")
	logging.warning("cam.py: WARNING: " + str(error))


class Camera:
	"""
    Object to get data from Realsense Camera
    """
	def __init__(self,save_images = False,t_save_frame=5,output_dir='./trials/'):
		"""
	    Intitalize Camera object 
	    """
		self.save_images = save_images
		self.clock = time.time()
		self.t_save_frame = t_save_frame
		self.output_dir = output_dir
		self.data_dir = path.join(self.output_dir,"{}".format(time.strftime("%d_%b_%Y_%H:%M", time.gmtime())))
		if self.save_images:	
			ensureDir(self.data_dir)
		pass

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

	def reduceFrame(self, depth, height_ratio=.5, sub_sample=.3, reduce_to = 'lower'):
		"""
	    Takes in a depth image and removes 0 and values bigger than max_val
	    Will also crop image to be last h rows
	    """
		depth_copy = depth.copy()
		height = depth_copy.shape[0]
		h = int(height_ratio*(height))

		if reduce_to == 'lower':
			d_short = depth_copy[h:, 10:-10]
			d_short[d_short <= 0] = np.nan
			d_short[d_short > 4] = np.nan
		elif reduce_to == 'middle_lower':
			upper_brdr = 3*int(round((height-h)/4.0,0))
			lower_brdr = upper_brdr + h
			d_short = depth_copy[upper_brdr:lower_brdr, 10:-10]
			d_short[d_short <= 0] = np.nan
			d_short[d_short > 4] = np.nan
		elif reduce_to == 'middle':
			upper_brdr = int(round((height-h)/2.0,0))
			lower_brdr = upper_brdr+h
			d_short = depth_copy[upper_brdr:lower_brdr, 10:-10]
			d_short[d_short <= 0] = np.nan
			d_short[d_short > 4] = np.nan
		elif reduce_to == 'middle_upper':
			upper_brdr = int(round((height-h)/4.0,0))
			lower_brdr = upper_brdr+h
			d_short = depth_copy[upper_brdr:lower_brdr, 10:-10]
			d_short[d_short <= 0] = np.nan
			d_short[d_short > 4] = np.nan
		elif reduce_to == 'upper':
			d_short = depth_copy[:(height-h), 10:-10]
			d_short[d_short <= 0] = np.nan
			d_short[d_short > 4] = np.nan

		rescaled = rescale(d_short, sub_sample)
		
		if self.save_images and (time.time() - self.clock > self.t_save_frame):
			np.save(path.join(self.data_dir,str(time.time())),rescaled)
			self.clock = time.time()

		return rescaled

	def getFrames(self, frames=5, rgb=False):
		"""
	    Function will retrieve depth frames (and rgb if true) from R200 input
	    Cleans and averages depth images and scales down by sub_sample
	    """
		self.dev.wait_for_frames()

		depth = self.dev.depth*self.dev.depth_scale

		for _ in range(frames-1):
			self.dev.wait_for_frames()
			curr = self.dev.depth*self.dev.depth_scale
			depth = np.dstack((depth, curr))

		if frames != 1:
			depth = np.nanmean(depth, 2)

		depth[depth > 4] = np.nan

		if rgb:
			col = self.dev.color 
			return depth, col

		return depth

	def getFramesFromFile(self, filename, idx=None):
		"""
		BROKEN FIX SOON BROKEN FIX SOON BROKEN FIX SOON

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

		for i in range(frames-1):
			idy = idx+i+1
			s = np.load(df % idy)/1000.
			d = np.dstack((d, s))

		if frames != 1:
			d = np.nanmean(d, 2)
		d[d > 4] = np.nan

		return d, col


if __name__ == "__main__":
    """
    Application example with visualization.
    """
    import matplotlib.pyplot as plt
    import time

    cam = Camera()
    cam.connect()
    time.sleep(2)

    d = cam.getFrames()
    d_small = reduceFrame(d)


    plt.subplot(2, 1, 1)
    plt.imshow(d)

    plt.subplot(2, 1, 2)
    plt.imshow(d_small)

    plt.show()




