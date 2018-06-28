"""
Author: Jan Bernhard
Last updated: 03/20/18
Purpose: Gather sample RGB and depth images with the R200.
"""

import numpy as np
import os
import time 
import pyrealsense as pyrs
serv = pyrs.Service()
dev = serv.Device(device_id=0, streams=[pyrs.stream.DepthStream(fps=60), pyrs.stream.ColorStream(fps=60)])

path = './sample_data'
counter  = 0
while(True):
    try:
        counter += 1
        dev.wait_for_frames()
        d = dev.depth * dev.depth_scale * 1000  #16 bit numbers
        gray = np.expand_dims(d.astype(np.uint8), axis=2)
        f = os.path.join(path,"1_%d_d.npy"%(counter))
        np.save(f,d)
        col = dev.color
        f = os.path.join(path,"1_%d_c.npy"%(counter))
        np.save(f,col)
        #time.sleep(0.1)
    except KeyboardInterrupt:
        break


