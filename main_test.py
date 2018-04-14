# !#/usr/bin/env python
'''
Author: Viveque Ramji
Purpose: Main script to bring all modules together

'''
import numpy as np
import time
import logging

from robot_control import robot
from robot_control import head
from navigation import nav, adaptive_grid_sizing as ags
from vision import cam

MAX_DIST = 1.

def searchForGap(c,n,h,head_offset):
	'''
	Will check if the head was used to find gap and will adjust body rotation to follow head.
	'''
	angle = 0
	found_gap = False
	for i in range(2*int(90/5)):
		#decide on turning direction
		if i%2 == 0:
			direction = 1 # right
			angle += 5*direction	
		else:
			direction = 1 # right
			angle = angle*direction
		#turn head
		completed_movement = False
		while(not completed_movement):
			completed_movement = h.look(turn=angle)
		#check for gap
		depth, _ = c.getFrames(1)
		d_red = c.reduceFrame(depth)

		x = n.reconstructFrame(d_red)
		frac, _ = n.obstacleAvoid(x,MAX_DIST)
		if frac is not None:
			found_gap = True
			break

	# reset head position
	turned = False
	while(not turned):
		turned = h.look(turn=0.0)
	if found_gap:
		gap_direction = 1 if angle > 0 else -1
		return gap_direction
	else:
		return


def sendDirection(n,r,fracx,depth_image):
	gap_direction = 0 #Camera starts pointing straight ahead 
	# when head was used to find a gap
	frac_prime = None
	if gap_direction != 0:
		frac_prime, _ = n.obstacleAvoid(depth_image, 0.7) # avoid running into obstacle straight ahead
		if fracx != None:
			gap_direction = 0 #reset turning rate
	

	if fracx is None and gap_direction == 0:
		print('Warning: No path straight ahead. Using head to find path')
		#n.plot(rgb, depth, x, 0)
		posx = 10
		r.testMove()
		# gap_direction = searchForGap(c,n,h,gap_direction)
	
	elif(fracx is None and frac_prime is None):
		print("Error: cannot find where to walk")
		r.testMove()

	elif(gap_direction != 0):
		#max turning rate in gap_direction

		r.testMove(forward=0.3, turn=gap_direction*0.6)

	else:
		print("Rotate {:.1f} fraction".format(fracx))
		# n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)
		# posx = (1+fracx)*rgb.shape[1]/2
		r.testMove(forward=0.3, turn=round(0.6*fracx,1))

	return True

def online(c, n, r, h):
	'''
	Will continuously to get depth images from camera and then plot rgb,
	original depth, interpolated depth, and the point where the robot is told
	to move until keyboard interrupt
	'''
	c.connect()
	r.connect()
	h.connect()
	
	counter = 0
	fractions = []
	try:
		time.sleep(1)
		while True:
			counter += 1
			depth, rgb = c.getFrames(1)

			d_red = c.reduceFrame(depth)

			t = time.time()
			x = n.reconstructFrame(d_red)
			print("Time to reconstruct using rbf: ", time.time()-t)
			t = time.time()
			y = ags.depth_completion(x, .2)
			print("Time to reconstruct using ags: ", time.time()-t)
			t = time.time()

			if x is None:
				print("Error, cannot find where to walk")
				continue

			# fracx, _ = n.obstacleAvoid(x, MAX_DIST)
			fracx = 0
			fracy, _ = n.obstacleAvoid(y, MAX_DIST)

			fractions.append(fracy)

			if counter == 5:
				fractions.sort()
				# fractions = fractions[1:-1]
				fracx = round(sum(fractions)/float(len(fractions)),2)

				if fracx is None:
					posx = 0
				else:
					posx = (1+fracx)*rgb.shape[1]/2

				if fracy is None:
					posy = 0
				else:
					posy = (1+fracy)*rgb.shape[1]/2

				n.plot(rgb, depth, x, posx, y, posy, b=1)
				sendDirection(n,r,fracx,y)
				#reset
				fractions = []
				counter = 0



			

	except KeyboardInterrupt:
		logging.warning("Main.py: KeyboardInterrupt")
		c.disconnect()
		r.disconnect()
		h.disconnect()
		pass

def offline(c, n, r):
	'''
	Offline version to load saved images and plot where the robot should move
	'''
	# import os

	# sample_dir = './data/sample_data_mounted_camera'
	# for filename in os.listdir(sample_dir):
	for i in range(200, 450, 10):
		t = time.time()
		filename = './data/sample_data_mounted_camera/1_%d_'
		depth, rgb = c.getFramesFromFile(filename, i)
		print("ME")
		d_red = c.reduceFrame(depth)
		print("Time to load images: ", time.time()-t)

		t = time.time()
		
		x = n.reconstructFrame(d_red)
		print("Time to reconstruct using rbf: ", time.time()-t)

		t = time.time()

		y = ags.depth_completion(d_red)
		print("Time to reconstruct using ags: ", time.time()-t)

		global MAX_DIST
		MAX_DIST = 0.7
		fracx, degx = n.obstacleAvoid(x, MAX_DIST)
		fracy, degy = n.obstacleAvoid(y, MAX_DIST)

		if fracx is None:
			posx = 10
		else:
			posx = (1+fracx)*rgb.shape[1]/2
		if fracy is None:
			posy = 10
		else:
			posy = (1+fracy)*rgb.shape[1]/2
		
		# n.plot(rgb, depth, x, posx, y, posy, b=1)



def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)

	c = cam.Camera(sub_sample=0.3, height_ratio=0.3, frames = 2)
	n = nav.Navigation(perc_samples=0.01)
	r = robot.Robot()
	h = head.Head()


	PORT = '/dev/ttyUSB0'
	BAUDERATE = 115200
	r.connect(PORT,BAUDERATE)

	on = True

	if on:
		online(c, n, r, h)
	else:
		offline(c, n, r)
	

if __name__== "__main__":
  main()

