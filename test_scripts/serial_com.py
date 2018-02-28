import logging
logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs

import serial
import getch

forward = True

# Config Constants (Later export to .json file)
PORT = '/dev/ttyUSB0' # dmesg | grep tty
BAUDERATE = 115200
TIMEOUT = 2 # set to 1 for normal use, 2 for debugging

serv = pyrs.Service()
dev = serv.Device()

ser = serial.Serial(PORT,BAUDERATE,timeout = TIMEOUT)

dev.apply_ivcam_preset(0)

cnt = 0
last = time.time()
smoothing = 0.9
fps_smooth = 30
msg = 90130000
count =0
walking = False

def stand():
    ser.write(str.encode("90000000"))
    read = None
    while(read != b'next\n'):
        read = ser.readline()
        print(read)

def walk(direction):
    if direction == 'f':
        string = "90130000"
    else :
        string = "90030000"
    ser.write(str.encode(string))
    read = None
    while(read != b'next\n'):
        read = ser.readline()
        print(read)



while(True):
    if count < 50:
        stand()
        count += 1
        continue
        
    dev.wait_for_frames()

    d = dev.depth * dev.depth_scale * 1000 #16 bit numbers
    if np.amax(d) == 0:
        stand()
        walking = False
        print("STOPPING")
        continue

    # Add Error message for wrong command input
    string = str(msg)
    if(len(string) != 8): 
        assert len(string) != 8,'ERROR: Command string is not 8 bytes' 
        continue

    walking = True
    walk('f')
    