# Robot Control
Controls the Minitaur base and the rotational sensor mount with the `robot.py` and `head.py` scripts, respectively.

## Development status
#### Robot.py:
 - [x] function testing 
 - [x] object terminal testing
 - [x] object robot testing
 - [x] revise communication robustness
#### Head.py:
 - [x] add control code
 - [x] terminal testing of control code
 - [x] physical testing of control code
 - [ ] add functionality to differentiate between 2-DOF and 1-DOF design
#### V0.2: With logging capability and more robust functionality:
 - [x] add logging
 - [x] replace if-loops with try-except statements
 - [x] testing
 - [x] merge robot.py with robot_dev_wLog.py

## Setup
### Requirements:
- python3
- RPi ```sudo apt-get -y install python3-rpi.gpio``` (only for head.py)
- pyserial ```pip3 install pyserial```
- robot.py

## Example
```python
"""
Test routine: 
    -  walk forward 3sec and rotate head slightly up and right, 
    -  walk at higher standing height normal height 2sec 
        and turn head to starting position, 
    -  sit 2 sec,
    -  return to starting position
"""
import time
import robot_v2

# different for every computer
PORT = '/dev/ttyUSB0' # Realsense CPU
BAUDERATE = 115200
TIMEOUT = 1
obj = robot_v2.Robot()
obj.connect(PORT,BAUDERATE,TIMEOUT)
try:
    print(" >>> START TEST SEQUENCE <<<")
    print(">>> WALK <<<")
    for _ in range(30):
        obj.move(forward=0.3)
        time.sleep(0.1)
    print(">>> HIGH WALK, TURN RIGHT<<<")
    for _ in range(20):
        obj.move(forward=0.2,height=0.3,turn = 0.3)
        time.sleep(0.1)
    print(">>> SIT <<<")
    for _ in range (20):
        obj.move(height = -.9)
        time.sleep(0.1)
    print(">>> STAND <<<")
    for _ in range (20):
        obj.move()
        time.sleep(0.1)
    
    obj.disconnect()
    print(">>> TEST COMPLETE <<<")
    
except KeyboardInterrupt:
    obj.disconnect()    
    print("Test ended prematurely and has been disconnected")
```

