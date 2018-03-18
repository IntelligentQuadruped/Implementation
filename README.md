# Robot Control
High-level control commands for the quadruped.

## Development status
#### Main body motion control:
 - [x] function testing 
 - [x] object terminal testing
 - [x] object robot testing
#### Head unit control:
 - [x] add control code
 - [x] terminal testing of control code
 - [x] physical testing of control code
#### V0.2: With logging capability and more robust functionality:
 - [x] add logging
 - [x] replace if-loops with try-except statements
 - [ ] testing
 - [ ] merge robot.py with robot_dev_wLog.py

## Setup
### Requirements:
- python3
- RPi ```sudo apt-get -y install python3-rpi.gpio``` (only for robot_dev.py)
- pyserial ```pip3 install pyserial```
- robot.py

## Example
```python
"""
Test routine: 
    - walk forward 3sec, 
    - walk at higher standing height normal height 2sec, 
    - sit 2 sec,
    - return to starting position
"""
import robot
import time

# different for every computer
PORT = '/dev/<Your USB Port Address>'
# Serial parameters
BAUDERATE = 115200
TIMEOUT = 1

obj = robot.Robot()
obj.connect(PORT,BAUDERATE,TIMEOUT)

print(" >>> START TEST SEQUENCE <<<")
print(">>> WALK <<<")
for _ in range(30):
    obj.command(forward=0.3)
    time.sleep(0.1)

print(">>> HIGH WALK <<<")
for _ in range(20):
    obj.command(forward=0.2, height=0.3)
    time.sleep(0.1)

print(">>> SIT <<<")
for _ in range (20):
    obj.command(height=-.9)
    time.sleep(0.1)

print(">>> STAND <<<")
for _ in range (20):
    obj.command()
    time.sleep(0.1)

obj.disconnect()
print(">>> TEST COMPLETE <<<")
```

