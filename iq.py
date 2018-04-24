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
from config import *


class IntelligentQuadruped:

	def __init__(self):
		self.r = robot.Robot()
		self.h = head.Head()
		self.c = cam.Camera()
		self.n = nav.Navigation(debug=DEBUG)
		self.average = deque(maxlen=N_AVERAGE_DIRECTIONS)

	def connect(self, port, bauderate):
		self.r.connect(port, bauderate)
		self.c.connect()
		self.h.connect()

	def disconnect(self):
		self.r.disconnect()
		self.c.disconnect()
		self.h.disconnect()

	def filterOutlier(self, z_score_threshold):
		"""
		Filters out outliers using the modified Z-Score method.
		"""
		data = np.array(self.average)
		median = np.median(data)
		deviation = np.median(np.abs(data - median))
		z_scores = 0.675*(data - median)/deviation
		data_out = data[np.where(np.abs(z_scores) < z_score_threshold)].tolist()
		output = data_out if len(data_out) > 0 else self.average
		return output

	def sendDirection(self, frac):
		self.r.move(forward=FORWARD, turn=round(frac,1))


	def run(self):
		depth, col = self.c.getFrames(FRAMES_AVRGD, rgb=True)

		depth_reduced = self.c.reduceFrame(depth, HEIGHT_RATIO, SUB_SAMPLE)

		t = time.time()
		adapted = self.n.reconstructFrame(depth_reduced, PERC_SAMPLES, MIN_AGS_SIGMA, MIN_AGS_H)
		print(time.time() - t)
		
		if adapted is None:
			self.average.clear()
			self.r.move()
			print("Error, cannot find where to walk")
			return

		pos = self.n.obstacleAvoid(adapted, MAX_DIST)
		
		if pos is None:
			self.average.clear()
			self.r.move()
			print("Error, cannot find where to walk")
		
		else:
			self.average.append(pos)
			if len(self.average) == N_AVERAGE_DIRECTIONS:
				outliers_removed = self.filterOutlier(Z_SCORE_THRESHOLD)
				mean = np.mean(outliers_removed)
				frac = 2.*mean/adapted.shape[1] - 1
				frac = round(frac, 1)
				print("frac {}".format(frac))

				self.sendDirection(frac)
		if DEBUG:
			print(pos, adapted.shape[1])
			self.n.plot(depth, col, depth, adapted)



def main():
	logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)

	iq = IntelligentQuadruped()

	iq.connect(PORT, BAUDERATE)

	time.sleep(INITIAL_DELAY)

	while(True):
		try:
			iq.run()

		except KeyboardInterrupt:
			logging.warning("Iq.py: KeyboardInterrupt")
			iq.disconnect()

	

if __name__== "__main__":
  main()














