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
		self.c = cam.Camera(SAVE_FRAME,SAVE_FRAME_INTERVAL,OUTPUT_DIR)
		self.n = nav.Navigation(debug=DEBUG)
		self.average = deque(maxlen=N_AVERAGE_DIRECTIONS)
		self.barrier_count = 0
		self.t_process = time.time()

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
		turn = (abs(frac)/0.9)*(MAX_TURN - MIN_TURN) + MIN_TURN
		turn = round(turn*np.sign(frac), 1)
		print("Turning Rate {}".format(turn))
		self.r.move(forward=FORWARD, turn=frac)
		print("Processing time: %.4f"%(time.time()-self.t_process))
		self.t_process = time.time()


	def run(self):
		depth, col = self.c.getFrames(FRAMES_AVRGD, rgb=True)

		depth_reduced = self.c.reduceFrame(depth, HEIGHT_RATIO, SUB_SAMPLE,NAV_FOCUS)

		# t = time.time()
		adapted = self.n.reconstructFrame(depth_reduced, PERC_SAMPLES, MIN_AGS_SIGMA, MIN_AGS_H, ALGORITHM)
		# print(time.time() - t)
		
		if adapted is None:
			self.average.clear()
			self.r.move()
			print("Error, cannot find where to walk")
			return

		pos = self.n.obstacleAvoid(adapted, MAX_DIST)

		if pos is None or pos == np.inf:
			frac = 0.0
			self.barrier_count =+ 1
		else:
			frac = 2.*pos/adapted.shape[1] - 1
		self.average.append(frac)

		if self.barrier_count >= 3:
			print("Error, cannot find where to walk")
			#stop and regroup
			start=time.time()
			while(time.time()-start < 2.0):
				self.r.move()
			self.average.clear()
			self.barrier_count = 0
			

		
		
		if len(self.average) == N_AVERAGE_DIRECTIONS:
			outliers_removed = self.filterOutlier(Z_SCORE_THRESHOLD)
			mean = round(np.mean(outliers_removed), 1)
			print('mean',mean)
			self.sendDirection(mean)
			# self.average.clear()

		if DEBUG:
			print(pos, adapted.shape[1])
			self.n.plot(depth, col, depth, adapted)



def main():
	logging.basicConfig(filename="./Logs/Control_Log_{}.log".format(time.ctime()),
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
			iq.r.move()
			logging.warning("Iq.py: KeyboardInterrupt")
			iq.disconnect()

	

if __name__== "__main__":
  main()




  
