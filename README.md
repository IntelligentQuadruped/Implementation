# Intelligent Quadruped Implementation

## Setup
### Requirements
Dependencies beyond the **Python 2.7** standard library:
* numpy
* matplotlib
* pyrealsense 1.16
* RPi.GPIO
* skimage
* OpenCV

## Structure

### Configuration file
All parameters that can be changed to impact the results are collected in the `config.py` script.

Parameter Name | Description
-------------- | -----------
DEBUG | 
INITIAL_DELAY | 
HEAD_CONNECTED | 
N_AVERAGE_DIRECTIONS | 
Z_SCORE_THRESHOLD | 
PORT | 
BAUDERATE | 
FORWARD | 
MAX_TURN | 
MIN_TURN | 
WALKING_HGHT | 
MAX_DEPTH | 
FRAMES_AVRGD | 
HEIGHT_RATIO | 
SUB_SAMPLE | 
SAVE_FRAME | 
SAVE_FRAME_INTERVAL | 
OUTPUT_DIR | 
MAX_DIST | 
BARRIER_HEIGHT | 
PERC_SAMPLES | 
MIN_AGS_SIGMA | 
MIN_AGS_H | 
NAV_FOCUS |
ALGORITHM | 

### Modules 
![Code Structure](/Module_Structure.png)

## Future Steps

![alt tag](https://github.com/IntelligentQuadruped/Implementation.gif)

## Video of selected physical trials: [Link to Video](https://youtu.be/LM8ooHoOcEU)
NOTE: The video can only be accessed via a Google account registered with a princeton.edu email address.
