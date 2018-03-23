'''
Author: Viveque Ramji
Purpose: Main script to bring all modules together

'''

import cv2
import numpy as np
import time
import logging

import robot
import nav
import cam


def online(c, n):
	'''
	Will continuously to get depth images from camera and then plot rgb,
	original depth, interpolated depth, and the point where the robot is told
	to move until keyboard interrupt
	'''
	c.connect()

	try:
		while True:
			t = time.time()
			depth, rgb = c.get_frames(1)
			x = n.reconstruct_frame(depth)
			if x is None:
				print("Error, caannot find where to walk")
				continue
			max_dist = 1.2
			frac, deg = n.obstacle_avoid(x, max_dist)
			print("Time: ", time.time()-t)
			if frac == None:
				print("Error: cannot find where to walk")
				n.plot(rgb, depth, x, 0)
				r.test_move()
			else:
				print("Rotate {:.1f} fraction".format(frac))
				n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)
				r.test_move(forward=0.3, turn=0.6*frac)

	except KeyboardInterrupt:
		logging.warning("Main.py: KeyboardInterrupt")
		c.disconnect()
		pass

def offline(c, n):
	'''
	Offline version to load saved images and plot where the robot should move
	'''

	t = time.time()
	filename = 'npz/%d_c_5d.npz' % 1
	
	depth, rgb = c.get_frames_from_file(filename)

	x = n.reconstruct_frame(depth)
	max_dist = 1.2
	frac, deg = n.obstacle_avoid(x, max_dist)

	print("Time: ", time.time()-t)
	if frac == None:
		print("Error: cannot find where to walk")
		n.plot(rgb, depth, x, 10)
	else:
		print("Rotate {:.1f} degree".format(deg))
		n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)



def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)

	c = cam.Camera(subSample=0.3, height_ratio=0.3)
	n = nav.Navigation(percSamples=0.3)
	r = robot.Robot()

	# PORT = '/dev/ttyUSB0'
	# BAUDERATE = 115200
    # r.connect(PORT,BAUDERATE)

	on = True

	if on:
		online(c, n)
	else:
		offline(c, n)
	

if __name__== "__main__":
  main()

