'''
Author: Viveque Ramji
Purpose: Main script to bring all modules together

'''
import numpy as np
import time
import logging
from collections import deque

from robot_control import robot
from robot_control import head
from navigation import nav
from vision import cam

class IntelligentQuadruped:

	def __init__(self):
		self.r = robot.Robot()
		self.h = head.Head()
		self.c = cam.Camera()
		self.h = nav.Navigation(debug=True)
		self.average = deque(maxlen=5)

	def connect(self, port, bauderate):
		self.r.connect(port, bauderate)
		self.c.connect()
		self.h.connect()

	def disconnect(self):
		self.r.disconnect()
		self.c.disconnect()
		self.h.disconnect()


	def sendDirection(self, frac):
		self.r.move(forward=0.2, turn=round(frac,1))


	def run(self):
		depth = self.c.getFrames()
		depth_reduced = self.c.reduceFrame(depth, sub_sample=0.5)

		adapted = self.n.reconstructFrame(depth_reduced)
		pos = self.n.obstacleAvoid(adapted, max_dist=1)

		if pos is None:
			self.average.clear()
			self.r.move()
			print("Error, cannot find where to walk")
			continue

		else:
			self.average.append(pos)
			if len(self.average) == 5:
				mean = np.mean(self.average)
				frac = 2.*mean/adapted.shape[1] - 1
				self.sendDirection(frac)


def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)

	iq = IntelligentQuadruped()

	PORT = '/dev/ttyUSB0'
	BAUDERATE = 115200
	iq.connect(PORT, BAUDERATE)

	while(True):
		try:
			iq.run()

		except KeyboardInterrupt:
			iq.disconnect()

	

if __name__== "__main__":
  main()














