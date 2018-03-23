import matplotlib.pyplot as plt
import numpy as np
import time

# import robot
import nav
import cam

def online(c, n):
	c = cam.Camera()
	c.connect()

	n = nav.Navigation()
	ax1 = plt.subplot(2,2,1)
	ax2 = plt.subplot(2,2,2)
	ax3 = plt.subplot(2,2,3)

	im1 = ax1.imshow()
	im2 = ax2.imshow()
	im3 = ax3.imshow()

	plt.ion()
	try:
		while True:
			t = time.time()
			depth, rgb = c.get_frames(True)
			x = n.reconstruct_frame(depth)
			max_dist = 1
			frac, deg = n.obstacle_avoid(x, max_dist)
			print("Time: ", time.time()-t)
			if frac == None:
				print("Error, caannot find where to walk")
				r.move()
			else:
				print("Rotate {:.1f} fraction".format(frac))
				r.move(forward=0.3, turn=0.6*frac)

			im1.set_data(rgb)
			im1.scatter((1+frac)*rgb.shape[1]/2, 460)
			im2.set_data(depth)
			im3.set_data(x)


	except KeyboardInterrupt:
		c.disconnect()
		pass

def offline(c, n):
	t = time.time()
	filename = 'npz/%d_c_5d.npz' % 1
	
	depth, rgb = c.get_frames_from_file(filename)

	x = n.reconstruct_frame(depth)
	max_dist = 1.2
	frac, deg = n.obstacle_avoid(x, max_dist)

	print("Time: ", time.time()-t)
	if frac == None:
		print("Error, cannot find where to walk")
		n.plot(rgb, depth, x, 10)
	else:
		print("Rotate {:.1f} degree".format(deg))
		n.plot(rgb, depth, x, (1+frac)*rgb.shape[1]/2)



def main():
	c = cam.Camera()
	n = nav.Navigation()
	# r = robot.Robot()

	PORT = '/dev/ttyUSB0'
	BAUDERATE = 115200
    # r.connect(PORT,BAUDERATE)

	online = False

	if online:
		online(c, n)
	else:
		offline(c, n)
	

if __name__== "__main__":
  main()
