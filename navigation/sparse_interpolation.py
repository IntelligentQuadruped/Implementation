'''
Author: Viveque Ramji
Purpose: Module to interpoalte values of depth matrix

'''
'''
***************************************************************************************/
*	 createSamples() and interpolateDepthImage() adapted from:
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

def createSamples(depth, perc_samples):
	"""
    Using perc_samples, return random number of samples from original data.
    Sparse identity matrices are used to conserve memory since identity
    matrices are mostly zeros.
    """
	height = depth.shape[0]
	width = depth.shape[1]
	N = height * width
	K = int(N * perc_samples)

	xGT = depth.flatten()
	rand = np.random.permutation(N)[:K]
	a = np.isnan(xGT[rand])
	samples = rand[np.nonzero(~a)[0]]

	Rfull = sparse.eye(N)
	R = Rfull.tocsr()[samples,:]
	measured_vector = R*xGT

	return samples, measured_vector


def interpolateDepthImage(shape, measured_vector, samples):
	"""
    Using just the original shape of depth image and random samples chosen,
    return a newly constructed depth image by interpolating known points.
    In this case use radial basis function after testing.
    """
	h = np.arange(0, shape[0])
	w = np.arange(0, shape[1])

	Yq, Zq = np.meshgrid(w, h)
	Y_sample = Yq.flatten()[samples]
	Z_sample = Zq.flatten()[samples]

	rbf1 = Rbf(Y_sample, Z_sample, measured_vector, function='linear')
	interpolated = rbf1(Yq, Zq)

	return interpolated



def main():
	import matplotlib.pyplot as plt


	depth = np.array([[np.nan, np.nan, 2, np.nan, 0, 1.2, np.nan, np.nan, 4], 
					  [.3, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 3, np.nan],
					  [np.nan, np.nan, 1, np.nan, np.nan, 0, np.nan, np.nan, np.nan],
					  [.2, np.nan, np.nan, np.nan, 1, np.nan, 0, 4, np.nan]])

	samples, measured = createSamples(depth, 1)
	interpolated = interpolateDepthImage(depth.shape, measured, samples)
	print("done")

	plt.subplot(2, 1, 1)
	plt.title('Original')
	plt.imshow(depth, cmap='viridis')
	
	plt.subplot(2, 1, 2)
	plt.title('Interpolated')
	plt.imshow(interpolated, cmap='viridis')

	plt.show()

if __name__== "__main__":
  main()






