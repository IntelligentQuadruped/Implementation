# Intelligent Quadruped Implementation
This repository holds all code developed in the context of the senior thesis project titled "*Intelligent Quadruped: Simplified RGBD-Based Autonomous Navigation for a Quadruped Robot*." The thesis project was submitted to the department of Mechanical and Aerospace Engineering of Princeton University in partial fullfilment of the requirements of undergraduate independent work. Multiple sensor platform variants were developed as part of the project. GhostRobotics' Minitaur is utilized during ongoing testing of the sensor platforms.
## Preview of physical application of code
Video of selected physical trials: [Link to Video](https://youtu.be/LM8ooHoOcEU)
NOTE: The video can only be accessed via a Google account registered with a princeton.edu email address.

## Setup
### Requirements
Dependencies beyond the **Python 2.7** standard library:
* numpy
* matplotlib
* pyrealsense 1.16
* RPi.GPIO
* skimage

## Structure

### Configuration file
All parameters that can be changed to impact the results are collected in the `config.py` script.

Parameter Name | Description
-------------- | -----------
DEBUG | If `True` displays frames of reconstruction and navigation processes
INITIAL_DELAY | Sets a time in seconds before the robots starts its behavior
HEAD_CONNECTED | Set `True` if you intend to turn the head
N_AVERAGE_DIRECTIONS | Number of commands averaged in queue 
Z_SCORE_THRESHOLD | Threshold value of test as float
PORT | USB-port address, Up-Board address comes standard
BAUDERATE | Communication rate of serial port
FORWARD | Set standard forward walking speed (0.0 to 0.8)
MAX_TURN | Maximum turning rate allowed (0.0 to 0.8)
MIN_TURN | Minimum turning rate to set for turning command (0.0 to 0.8)
WALKING_HGHT | Sets height of Minitaur walking height relative to neutral height (-0.8 to 0.8)
MAX_DEPTH | Maximum distance in meter for which the sensor is accurate (float)
FRAMES_AVRGD | Number of depth frames to be averaged at time of capture
HEIGHT_RATIO | Ratio to which the frame should be resized (float)
SUB_SAMPLE | 
SAVE_FRAME | Set `True` if you wish to save RGB and D frames during operation
SAVE_FRAME_INTERVAL | Set time between saved frames in seconds (float)
OUTPUT_DIR | Set directory of saved frames
MAX_DIST | Maximum distance in meter at which an object is considered an obstacle necessary to avoid
BARRIER_HEIGHT | Sets height of barrier relative to frame height
PERC_SAMPLES | 
MIN_AGS_SIGMA | Acceptable deviation within a single gridcell (float 0.1 to 1.0)
MIN_AGS_H | Minimum height of a gridcell in pixel
NAV_FOCUS | Reduces the region within the camera image for which obstacles are considered. Options are: 'upper','middle_upper', 'middle', 'middle_lower', 'lower'
ALGORITHM | Set the combination of reconstruction algortihms. Options are: 'rbf', 'voronoi', 'ags_only'

### Modules 
![Code Structure](/Module_Structure.png)

## How to execute
All files are found in main. After setting all parameters in configs/config.py, the behavior can be triggered by executing iq.py. 
```
sudo python iq.py
```
or if used together with the turning sensor platform
```
sudo python hiq.py
```

## Future Steps

- [ ] Calibrate turning behavior
- [ ] Improve application for turning head during normal walking operation
- [ ] Add memory capability to save previously observed obstacles
