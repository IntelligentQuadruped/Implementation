'''
Author: Viveque Ramji
Purpose: Main script to bring all modules together

'''
import numpy as np
import time
import logging

from robot_control import robot
from robot_control import head
from navigation import nav
from vision import cam


def online(c, n, r, h):
	'''
	Will continuously to get depth images from camera and then plot rgb,
	original depth, interpolated depth, and the point where the robot is told
	to move until keyboard interrupt
	'''
	c.connect()
	r.connect()
	h.connect()

	try:
		while True:
			t = time.time()
			depth, rgb = c.getFrames(1)
			x = n.reconstructFrame(depth)
			if x is None:
				print("Error, caannot find where to walk")
				continue
			max_dist = 1.2
			frac, deg = n.obstacleAvoid(x, max_dist)
			print("Time: ", time.time()-t)
			if frac is None:
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
		r.disconnect()
		h.disconnect()
		pass

def offline(c, n):
	'''
	Offline version to load saved images and plot where the robot should move
	'''

	t = time.time()
	filename = 'navigation/npz/%d_c_5d.npz' % 1
	
	depth, rgb = c.getFramesFromFile(filename)

	x = n.reconstructFrame(depth)
	max_dist = 1.2
	frac, deg = n.obstacleAvoid(x, max_dist)

	print("Time: ", time.time()-t)
	if frac is None:
		print("Error: cannot find where to walk")
		n.plot(rgb, depth, x, 10, b=1)
	else:
		print("Rotate {:.1f} degree".format(deg))
		n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2, b=1)



def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)

	c = cam.Camera(sub_sample=0.3, height_ratio=0.3)
	n = nav.Navigation(perc_samples=0.3)
	r = robot.Robot()
	h = head.Head()

	PORT = '/dev/ttyUSB0'
	BAUDERATE = 115200
	r.connect(PORT,BAUDERATE)

	on = False

	if on:
		online(c, n, r, h)
	else:
		offline(c, n)
	

if __name__== "__main__":
  main()

