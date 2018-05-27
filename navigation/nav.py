'''
Author: Viveque Ramji
Purpose: Module to clean camera data and provide an open direction to move in

'''
import numpy as np
from scipy import sparse
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


	def reconstructFrame(self, depth, perc_samples=0.005, min_sigma=0.5, min_h=10, algorithm_type='voronoi'):
		"""
	    Givena partial depth image, will return an interpolated version filling
	    all missing data.
	    """


		if algorithm_type == 'voronoi':
			samples, measured_vector = si.createSamples(depth, perc_samples)
			if len(samples) <= 1:
				return None
			filled = voronoi.getVoronoi(depth.shape, samples, measured_vector)
		elif algorithm_type == 'rbf':
			samples, measured_vector = si.createSamples(depth, perc_samples)
			if len(samples) <= 1:
				return None
			filled = si.interpolateDepthImage(depth.shape,samples, measured_vector)
		elif algorithm_type == 'ags_only':
			filled = depth

		adapted = ags.depthCompletion(filled, min_sigma, min_h)

		if self.debug:
			samples, measured_vector = si.createSamples(depth, perc_samples)
			sample_img = np.zeros((depth.shape)).flatten()
			sample_img[samples] = depth.flatten()[samples]
			sample_img = sample_img.reshape(depth.shape)

			self.plot(depth, sample_img, filled, adapted)

		return adapted
	def obstacleAvoid(self, depth, max_dist=1.2,barrier_h=.5):
		"""
	    Given a depth image and a threshold value, will find the largest gap
	    that can be used, returning the fraction along the images width where
	    this is and the degrees rotation from the center. 
	    """
		pos = oa.findLargestGap(depth, max_dist, barrier_h,DEBUG=self.debug)
		return pos

	def plot(self, depth, sample_img, filled, ags, cmap='viridis', b=True):
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
		plt.imshow(filled, cmap=cmap)
		plt.title('RBF, Voronoi, or None')
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
    adapted = nav.reconstructFrame(depth, .1, .5, 10)
    frac, pos = nav.obstacleAvoid(adapted, 1.3)
