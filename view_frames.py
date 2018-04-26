import matplotlib.pyplot as plt
import numpy as np
import os
import argparse


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
		plt.figure(file)
		plt.imshow(frame)
		plt.title('Frame {} of {}:{}'.format((i+1),l, file))
		plt.show()
	except KeyboardInterrupt:
		print("Terminated Show Early")
		break
