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

MAX_DIST = 1.2

def searchForGap(c,n,h,head_offset):
	'''
	Will check if the head was used to find gap and will adjust body rotation to follow head.
	'''
	angle = 0
	found_gap = False
	for i in range(2*(90/5)):
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
		x = n.reconstructFrame(depth)
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


def online(c, n, r, h):
	'''
	Will continuously to get depth images from camera and then plot rgb,
	original depth, interpolated depth, and the point where the robot is told
	to move until keyboard interrupt
	'''
	c.connect()
	r.connect()
	h.connect()
	gap_direction = 0 #Camera starts pointing straight ahead 
	try:
		while True:
			t = time.time()
			depth, rgb = c.getFrames(1)
			x = n.reconstructFrame(depth)
			if x is None:
				print("Error, cannot find where to walk")
				continue
			frac, _ = n.obstacleAvoid(x, MAX_DIST)
			# when head was used to find a gap
			frac_prime = None
			if gap_direction != 0:
				frac_prime, _ = n.obstacleAvoid(x, 0.7) # avoid running into obstacle straight ahead
				if frac != None:
					gap_direction = 0 #reset turning rate

			print("Time: ", time.time()-t)
			if frac is None and gap_direction == 0:
				print('Warning: No path straight ahead. Using head to find path')
				n.plot(rgb, depth, x, 0)
				r.test_move()
				gap_direction = searchForGap(c,n,h,gap_direction)
			
			elif(frac is None and frac_prime is None):
				print("Error: cannot find where to walk")
				r.test_move()

			elif(gap_direction != 0):
				#max turning rate in gap_direction
				r.test_move(forward=0.3, turn=gap_direction*0.6)

			else:
				print("Rotate {:.1f} fraction".format(frac))
				n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)
				r.test_move(forward=0.3, turn=round(0.6*frac,1))

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

	for _ in range(1):

		t = time.time()
		# filename = 'sample_obstacle_course/1_%d_' % (i+105)
		filename = 'navigation/npz/%d_c_5d.npz' % 5
		
		depth, rgb = c.getFramesFromFile(filename)

		x = n.reconstructFrame(depth)
		global MAX_DIST
		MAX_DIST = 0.8
		frac, deg = n.obstacleAvoid(x, MAX_DIST)

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

	c = cam.Camera(sub_sample=0.3, height_ratio=1)
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
		offline(c, n, r)
	

if __name__== "__main__":
  main()

