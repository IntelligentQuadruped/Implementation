'''
Author: Jan Bernhard
Purpose: Module to control the Princeton Minitaur robot research unit.
'''


# standard imports
import serial
import time
import logging


class Robot(object):
    """
    Object to control Minitaur Robot that reacts to 8 byte integer 
    move.
    """
    
    def __init__(self):
        self.current_command = None # stores most recent command
        pass

    def connect(self, usb_port_address, bauderate, time_out = 1):
        """
        Sets up the initial serial communication connection
        """

        logging.info("robot.py: Starts to connect components.")

        # connect components
        try:
            self.ser = serial.Serial(usb_port_address,
                                    bauderate, 
                                    timeout = time_out)
            self.connect_body = True # stores which components are connected.
            logging.info("robot.py: Body component connected")
        except:
            self.connect_body = False
            logging.warning("robot.py: Body component could not be connected.")

        logging.info("robot.py: Body = {}".format(self.connect_body))

        return
    
    def disconnect(self):
        """
        Disconnects the serial communication.
        """
        if self.connect_body:
            self.ser.close()

        logging.info("robot.py: Disconected body component successfully.")
        return

#--------------------------------------------------------------------
# Body Control
#--------------------------------------------------------------------

    def __convertToMove(self, float_in):
        """
        Takes in move in float form and encodes move as two digit string.
        """
        # logging.info("Converts move command to 8byte string")
        int_in = int(float_in * 10)
        first_digit = 0 if int_in < 0 else 1    #encodes negative
        second_digit = abs(int_in)              #only consider magnitude
        return (first_digit, second_digit)

    def move(self, **kwargs):
        """
        Controls main body translation.
        Converts command move input to 8 byte integer.

        Takes arguments as follows:
            behavior    [int]                      0 to 9,
            forward     [m/s]                   -0.9 to 0.9,
            turn        [rad/s]                 -0.9 to 0.9,
            height      [% relative to normal]  -0.9 to 0.9
        
        Returns:
            Bool that signifies if command was correctly received by Minitaur.
        """
        if self.connect_body is False:
            logging.warning("robot.py: Method move(): Cannot execute command. Body disconneted.")
            return

        new_move = list("90000000")

        for key in kwargs:
            if key == 'forward':
                new_move[2:4] = self.__convertToMove(kwargs[key])
            elif key == 'turn':
                new_move[4:6] = self.__convertToMove(kwargs[key])
            elif key == 'height':
                new_move[6:8] = self.__convertToMove(kwargs[key])
            elif key == 'behavior':
                new_move[1] = int(kwargs[key])

        new_move = map(str,new_move) # converting int to char
        new_move = ''.join(new_move) # joining char to str

        # Waiting for Signal that Minitaur is ready to receive move input
        read = None # Stores messages from Minitaur
        received = False # True iff the correct message was received
        while(read != b'next\n'):
            read = self.ser.readline()
            read = str(read, encoding) # converts bites to unicode str
            if str(self.current_command) in read:
                print(read)
                received = True
        
        # Sending new move string
        self.ser.write(str.encode(str(new_move)))

        # Through warning if move command wasn't correctly received by Minitaur
        if received is False:
            logging.warning("robot.py: Last Move command {} was not received by Minitaur."\
                            .format(self.current_command))

        # Update current move command and log command
        if self.current_command != new_move:
            self.current_command = new_move
            logging.info("robot.py: Move command sent: {}".format(new_move))
        
        return received


    def test_move(self, **kwargs):
        """
        Same as move but does not need connection/prints dummy responses
        Takes arguments as follows:
            behavior    [int]                      0 to 9,
            forward     [m/s]                   -0.9 to 0.9,
            turn        [rad/s]                 -0.9 to 0.9,
            height      [% relative to normal]  -0.9 to 0.9
        """

        new_move = list("90000000")

        for key in kwargs:
            if key == 'forward':
                new_move[2:4] = self.__convertToMove(kwargs[key])
            elif key == 'turn':
                new_move[4:6] = self.__convertToMove(kwargs[key])
            elif key == 'height':
                new_move[6:8] = self.__convertToMove(kwargs[key])
            elif key == 'behavior':
                new_move[1] = int(kwargs[key])

        new_move = map(str,new_move) # converting int to char
        new_move = ''.join(new_move) # joining char to str

        print("Move command sent: {}".format(new_move))


    
if __name__ == '__main__':
    """
    Test routine: 
     -  walk forward 3sec and rotate head slightly up and right, 
     -  walk at higher standing height normal height 2sec 
            and turn head to starting position, 
     -  sit 2 sec,
     -  return to starting position
    """
    # different for every computer
    PORT = '/dev/ttyUSB0' # Realsense CPU
    # PORT = '/dev/tty.usbserial-DN01QALN' # Jan's MB
    BAUDERATE = 115200
    TIMEOUT = 1
    obj = robot_v2.Robot()
    obj.connect(PORT,BAUDERATE,TIMEOUT)
    try:
        print(" >>> START TEST SEQUENCE <<<")
        print(">>> WALK & LOOK SLIGHTLY RIGHT, UP <<<")
        for _ in range(30):
            obj.move(forward=0.3)
            time.sleep(0.1)
        print(">>> HIGH WALK & LOOK FROM INITIAL POSITION <<<")
        for _ in range(20):
            obj.move(forward=0.2,height=0.3)
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
