import cam
import numpy as np
import os
import time 

c = cam.Camera(frames=1, height_ratio=1.0, sub_sample=1.0, max_val=4)
c.connect()
path = './sample_data'
counter  = 0
while(True):
    try:
        counter += 1
        depth_img = c.getFrames()
        f = os.path.join(path,"0%d_d.npy"%(counter))
        np.save(f,depth_img)
        time.sleep(0.5)
    except KeyboardInterrupt:
        break

c.disconnect()