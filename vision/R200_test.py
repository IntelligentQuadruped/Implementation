import logging
logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs


with pyrs.Service() as serv:
    with serv.Device() as dev:

        dev.apply_ivcam_preset(0)

        while True:

            dev.wait_for_frames()
            c = dev.color
            c = cv2.cvtColor(c, cv2.COLOR_RGB2BGR)
            d = dev.depth * dev.depth_scale * 1000
            d = cv2.applyColorMap(d.astype(np.uint8), cv2.COLORMAP_RAINBOW)

            cd = np.concatenate((c, d), axis=1)

            cv2.imshow('RGB+Depth', cd)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
