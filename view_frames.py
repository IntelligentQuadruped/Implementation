import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
from navigation import adaptive_grid_sizing as ags
from config import *

from navigation import voronoi
from navigation import sparse_interpolation as si
from navigation import obstacle_avoid as oa

parser = argparse.ArgumentParser()
parser.add_argument("data_directory", 
	help="Path to Directory with saved .npy files.", 
	type=str)
args = parser.parse_args()
dir_in = args.data_directory

l = len(os.listdir(dir_in))
for i, file in enumerate(os.listdir(dir_in)):
	path = os.path.join(dir_in,file)
	frame = np.load(str(path))
	try:
		recon = ags.depthCompletion(frame,MIN_AGS_SIGMA, MIN_AGS_H)
		samples, measured_vector = si.createSamples(frame, PERC_SAMPLES)
		filled = voronoi.getVoronoi(frame.shape, samples, measured_vector)
		voro = ags.depthCompletion(filled,0.1, 30)
		rbf_pre = si.interpolateDepthImage(frame.shape,samples, measured_vector)
		rbf = ags.depthCompletion(rbf_pre,0.2, 30)

		plt.subplot(2, 2, 1)
		plt.title('Depth')
		plt.imshow(frame)
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 2)
		plt.imshow(voro>MAX_DIST)
		plt.title('Voronoi')
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 3)
		plt.imshow(rbf>MAX_DIST)
		plt.title('RBF, Voronoi, or None')
		plt.xticks(visible=False)
		plt.yticks(visible=False)

		plt.subplot(2, 2, 4)
		plt.imshow(filled > MAX_DIST)
		plt.title('AGS')
		plt.xticks(visible=False)
		plt.yticks(visible=False)


		plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
		cax = plt.axes([0.85, 0.1, 0.075, 0.8])
		# plt.colorbar(cax=cax)

		plt.show()
	except KeyboardInterrupt:
		print("Terminated Show Early")
		break
