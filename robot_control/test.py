"""
Author: Jan Bernhard
Purpose: Full test sequence for Minitaur loaded with research platform.
"""

import robot_v2
import time

def main():
    # different for every computer
    PORT = '/dev/tty.usbserial-DN01QALN' 
    BAUDERATE = 115200
    TIMEOUT = 1
    obj = robot_v2.Robot()
    obj.connect(PORT,BAUDERATE,TIMEOUT)
    connection = False # Holds received message from Minitaur
    try:
        # Wait for successful communication to be established
        while(~connection):
            received = obj.move(height = .5) 
            connection = True if received is not None else False
            print(">>> Connecting... " + str(received))
    
        print(" >>> START TEST SEQUENCE <<<")
        print(">>> RAISE TO WALKING HEIGHT <<<")
        for _ in range(30):
            connection = obj.move(height = .2)
            if connection:
                print(">>> Successful Communication")
            else:
                print(">>> ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        print(">>> WALK FORWARD <<<")
        for _ in range(20):
            connection = obj.move(forward=0.4,height=0.2)
            if connection:
                print(">>> Successful Communication")
            else:
                print(">>> ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        print(">>> TURN RIGHT <<<")
        for _ in range (30):
            connection = obj.move(forward=.3,turn = .3, height = .2)
            if connection:
                print(">>> Successful Communication")
            else:
                print(">>> ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        print(">>> TURN LEFT <<<")
        for _ in range (30):
            connection = obj.move(forward=.3,turn = -0.3, height = .2)
            if connection:
                print(">>> Successful Communication")
            else:
                print(">>> ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        obj.move()
        obj.disconnect()
        print(">>> TEST COMPLETE <<<")
        
    except KeyboardInterrupt:
        obj.disconnect()    
        print("Test ended prematurely and has been disconnected")

if __name__ == "__main__":
    main()
