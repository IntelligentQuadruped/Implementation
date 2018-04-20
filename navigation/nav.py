'''
Author: Viveque Ramji
Purpose: Module to clean camera data and provide an open direction to move in

'''
import numpy as np
from scipy import sparse
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt

import adaptive_grid_sizing as ags
import voronoi
import sparse_interpolation as si
import obstacle_avoid as oa

import time
import logging

class Navigation:
	"""
    Object to use depth images to find gap to move in to.
    """

	def __init__(self, debug=False):
		"""
	    Intitalize Navigation module
	    """
		self.debug = debug


	def reconstructFrame(self, depth, perc_samples=0.1, min_sigma=0.3, min_h=10):
		"""
	    Givena partial depth image, will return an interpolated version filling
	    all missing data.
	    """
		samples, measured_vector = si.createSamples(depth, perc_samples)
		if len(samples) <= 1:
			return None

		vorn = voronoi.get_voronoi(depth.shape, samples, measured_vector)
		adapted = ags.depth_completion(vorn, min_sigma, min_h)

		if self.debug:
			sample_img = np.zeros((depth.shape)).flatten()
			sample_img[samples] = depth.flatten()[samples]
			sample_img = sample_img.reshape(depth.shape)

			self.plot(depth, sample_img, vorn, adapted)

		return adapted, vorn
	def obstacleAvoid(self, depth, max_dist=1.2):
		"""
	    Given a depth image and a threshold value, will find the largest gap
	    that can be used, returning the fraction along the images width where
	    this is and the degrees rotation from the center. 
	    """
		pos = oa.findLargestGap(depth, max_dist)
		if pos is None:
			return(None, None)
	  	
		frac = 2.*pos/depth.shape[1] - 1
		return (frac, pos)

	def plot(self, depth, sample_img, vorn, ags, cmap='viridis', b=True):
		"""
	    Will plot the rgb image, original depth, interpolated depth and the
	    position of where the algorithm recommends to move.
	    """
		plt.subplot(2, 2, 1)
		plt.title('Depth')
		plt.imshow(depth)
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 2)
		plt.imshow(sample_img, cmap=cmap)
		plt.title('Samples')
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 3)
		plt.imshow(vorn, cmap=cmap)
		plt.title('Voronoi')
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 4)
		plt.imshow(ags, cmap=cmap)
		plt.title('AGS')
		plt.xticks(visible=False)
		plt.yticks(visible=False)


		plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
		cax = plt.axes([0.85, 0.1, 0.075, 0.8])
		plt.colorbar(cax=cax)

		plt.show(block=~b)
		if b:
			time.sleep(b)
			plt.close()


if __name__ == "__main__":
    """
    Application example with visualization.
    """
    depth = np.random.rand(10, 5)
    depth = np.hstack((depth*4, depth*0.9))
    depth[0, 5] = np.nan
    depth[0, 6] = np.nan
    depth[depth>4.0] = 0.0

    nav = Navigation(True)
    adapted,vorn = nav.reconstructFrame(depth, perc_samples=.1)
    frac, pos = nav.obstacleAvoid(adapted, 1.3)









	  



















