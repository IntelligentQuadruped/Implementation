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
        while(connection==False):
            print("Connecting...")
            received = obj.move() 
            connection = True if received != None else False
            print(received)
    
        print(" >>> START TEST SEQUENCE <<<")
        # print(">>> WALK & LOOK SLIGHTLY RIGHT, UP <<<")
        # obj.look(turn=90,tilt=35)
        # for _ in range(30):
        #     obj.move(forward=0.3)
        #     time.sleep(0.1)
        # print(">>> HIGH WALK & LOOK FROM INITIAL POSITION <<<")
        # obj.look(turn=0,tilt=0)
        # for _ in range(20):
        #     obj.move(forward=0.2,height=0.3)
        #     time.sleep(0.1)
        print(">>> RAISE HEIGHT <<<")
        for _ in range (20):
            connection = obj.move(height = .3)
            if connection==True:
                print("Successful Communication")
            else:
                print("ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        print(">>> STAND <<<")
        for _ in range (20):
            connection = obj.move(height = .1)
            if connection==True:
                print("Successful Communication")
            else:
                print("ERROR: Unsuccessful Communication")
            time.sleep(0.1)
        
        obj.disconnect()
        print(">>> TEST COMPLETE <<<")
        
    except KeyboardInterrupt:
        obj.disconnect()    
        print("Test ended prematurely and has been disconnected")

if __name__ == "__main__":
    main()