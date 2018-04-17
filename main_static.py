# !#/usr/bin/env python
'''
Author: Viveque Ramji, Jan Bernhard
Purpose: Main script to bring all modules together for autonomous navigation.
		 Navigation case for 0 DOF in camera joint. 

'''
########### PARAMETERS TO CHECK BEFORE RUNNING SCRIPT #######################

DEBUG = True
MAX_DIST = 1. #meter
AGS_TOLERANCE = 0.2
# SAVE_SAMPLE = 2.0 # 1 saved frame every 2 seconds

# FOR ONLINE USE ONLY
ONLINE = False #Connected to components?
PORT = '/dev/ttyUSB0' #USB-port address
BAUDERATE = 115200
N_AVERAGE_DIRECTIONS = 5 # Number of averaged direction commands
INITIAL_DELAY = 10 #sec

# FOR OFFLINE USE ONLY
DATA_DIR = "./data/sample_data_mounted_camera"
N_FRAMES_TO_LOAD = 10
RANDOM_SELECTION = False


##################### MAIN SCRIPT ###########################################
import numpy as np
import time
import logging
from robot_control import robot
from robot_control import head
from navigation import nav
from navigation import adaptive_grid_sizing as ags
from vision import cam

def filterOutlier(data_list,z_score_threshold=3):
	"""
	Filters out outliers using the modified Z-Score method.
	"""
	data = np.array(data_list)
	median = np.median(data)
	deviation = np.median([np.abs(x - median) for x in data])
	z_scores = [0.675*(x - median)/deviation for x in data]
	data_out = data[np.where(np.abs(z_scores) < z_score_threshold)].tolist()
	output = data_out if len(data_out) > 0 else data_list
	return output

def sendDirection(n,r,fracx):

	# print(fracx)

	if fracx is None:
		print("Error: cannot find where to walk")
		r.move()

	else:
		print("Rotate {:.1f} fraction".format(fracx))
		# n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)
		# posx = (1+fracx)*rgb.shape[1]/2
		r.move(forward=0.2, turn=round(fracx,1))

	return True

def online(c, n, r, h):
	'''
	Will continuously to get depth images from camera and then plot rgb,
	original depth, interpolated depth, and the point where the robot is told
	to move until keyboard interrupt
	'''
	c.connect()
	h.connect()
	
	wall = 0
	counter = 0
	fractions = []

	try:
		time.sleep(INITIAL_DELAY)
		t_process = time.time()
		while True:
			counter += 1
			depth, rgb = c.getFrames(1)

			
			d_red = c.reduceFrame(depth)

			# t = time.time()
			x = n.reconstructFrame(d_red)
			# print("Time to reconstruct using rbf: ", time.time()-t)
			

			if x is None:
				r.move()
				print("Error, cannot find where to walk")
				continue

			# t = time.time()
			y = ags.depth_completion(x, AGS_TOLERANCE)
			# print("Time to reconstruct using ags: ", time.time()-t)
			# t = time.time()
			fracy, _ = n.obstacleAvoid(y, MAX_DIST)
			wall = wall + 1 if fracy is None else wall
			fracy = 0 if fracy is None else fracy
			fractions.append(fracy)

			if counter >= N_AVERAGE_DIRECTIONS:
				if wall == counter:
					r.move()
					print("Error: wall infront")
					continue
				
				fractions = filterOutlier(fractions)
				fracx = round(sum(fractions)/float(len(fractions)),2)

				if fracx is None:
					posx = 0
				else:
					posx = (1+fracx)*rgb.shape[1]/2

				if fracy is None:
					posy = 0
				else:
					posy = (1+fracy)*rgb.shape[1]/2

				# n.plot(rgb, depth, x, posx, y, posy, b=1)
				sendDirection(n,r,fracx)
				#reset
				fractions = []
				counter = 0
				wall = 0
				print("Processing time: %.4f"%(time.time()-t_process))
				t_process = time.time()

	except KeyboardInterrupt:
		logging.warning("Main.py: KeyboardInterrupt")
		c.disconnect()
		r.disconnect()
		h.disconnect()
		pass

def offline(c, n, r):
	'''
	Offline version to load saved images and plot where the robot should move.
	Can be run on any computer with skimage,numpy,matplotlib installed.
	'''
	import os
	import random

	paths = os.listdir(DATA_DIR)
	n_items = len(paths)
	if RANDOM_SELECTION:
		frames = random.sample(paths,N_FRAMES_TO_LOAD)
	else:
		index = np.linspace(0,n_items-1,N_FRAMES_TO_LOAD).tolist()
		frames = [os.listdir(DATA_DIR)[int(i)] for i in index]
	


	for filename in frames:
		filename = os.path.join(DATA_DIR,filename[:-5])
		print(filename)
		t = time.time()
		depth, rgb = c.getFramesFromFile(filename)
		print("ME")
		d_red = c.reduceFrame(depth)
		print("Time to load images: ", time.time()-t)

		t = time.time()
		x = n.reconstructFrame(d_red)
		print("Time to reconstruct using rbf: ", time.time()-t)

		if x is None:
			# r.testMove()
			print("Error, cannot find where to walk")
			continue

		t = time.time()
		y = ags.depth_completion(x, AGS_TOLERANCE)
		print("Time to reconstruct using ags: ", time.time()-t)

		fracx, _ = n.obstacleAvoid(x, MAX_DIST)
		fracy, _ = n.obstacleAvoid(y, MAX_DIST)

		# fracy, _ = n.obstacleAvoid(y, MAX_DIST)
		# fracy = 0 if fracy is None else fracy
		# fractions.append(fracy)

		# if counter >= N_AVERAGE_DIRECTIONS:
		# 	fractions = filterOutlier(fractions)
		# 	fracx = round(sum(fractions)/float(len(fractions)),2)

		if fracx is None:
			posx = 10
		else:
			posx = (1+fracx)*rgb.shape[1]/2
		if fracy is None:
			posy = 10
		else:
			posy = (1+fracy)*rgb.shape[1]/2
		n.plot(rgb, depth, x, posx, y, posy, b=1)

def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)
	c = cam.Camera(sub_sample=0.3, height_ratio=0.3, frames = 2)
	n = nav.Navigation(perc_samples=0.01)
	r = robot.Robot()
	h = head.Head()

	r.connect(PORT,BAUDERATE)

	n.DEBUG = DEBUG # Turns Obstacle plotting on/off

	if ONLINE:
		online(c, n, r, h)
	else:
		offline(c, n, r)
	

if __name__== "__main__":
  main()

