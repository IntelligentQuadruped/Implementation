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
DEBUG | Displays frames of reconstruction and navigation processes
INITIAL_DELAY | Sets a time in seconds before the robots starts its behavior
HEAD_CONNECTED | Set `True` if you intend to turn the head
N_AVERAGE_DIRECTIONS | Number of commands averaged in queue
Z_SCORE_THRESHOLD | Threshold value of test as float
PORT | USB-port address, Up-Board address comes standard
BAUDERATE | Communication rate of serial port
FORWARD | Set standard forward walking speed
MAX_TURN | Maximum turning rate allowed
MIN_TURN | Minimum turning rate to set for turning command
WALKING_HGHT | Sets height of Minitaur walking height relative to neutral height (-0.9 to 0.9)
MAX_DEPTH | Maximum depth value to for which the sensor is accurate
FRAMES_AVRGD | Number of depth frames to be averaged at time of capture
HEIGHT_RATIO | Ratio to which the frame should be resized (float)
SUB_SAMPLE | 
SAVE_FRAME | `True` if you wish to save RGB and D frames during operation
SAVE_FRAME_INTERVAL | Set time between saved frames in seconds (float)
OUTPUT_DIR | Set directory of saved frames
MAX_DIST | Maximum distance at which an object is considered an obstacle necessary to avoid
BARRIER_HEIGHT | Sets height of barrier relative to frame height
PERC_SAMPLES | 
MIN_AGS_SIGMA | Acceptable deviation within a single gridcell (float 0.1-1.0)
MIN_AGS_H | Minimum size of a gridcell
NAV_FOCUS | Reduces the region within the camera image for which obstacles are considered. Options are: 'upper','middle_upper', 'middle', 'middle_lower', 'lower'
ALGORITHM | Set the combination of reconstruction algortihms. Options are: 'rbf', 'voronoi', 'ags_only'

### Modules 
![Code Structure](/Module_Structure.png)

## Future Steps

![alt tag](https://github.com/IntelligentQuadruped/Implementation.gif)

## Video of selected physical trials: [Link to Video](https://youtu.be/LM8ooHoOcEU)
NOTE: The video can only be accessed via a Google account registered with a princeton.edu email address.
