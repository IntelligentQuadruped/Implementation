'''
Author: Jan Bernhard
Purpose: Module to control the Princeton Minitaur robot research unit.
'''


# standard imports
import serial
import time

import logging
# Setup of logging
logging.basicConfig(filename="Control_Log_{}.log".format(time.ctime()),
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%I:%M:%S',
                    level=logging.DEBUG)
try:
    import RPi.GPIO as GPIO
except:
    logging.warning("Could not import RPi module.")

# Global Constants
CONVERSION_FACTOR_TURN = 2.22 #steps per degree
CONVERSION_FACTOR_TILT = 10.0 #steps per degree

class Robot(object):
    """
    Object to control Minitaur Robot that reacts to 8 byte integer 
    move.
    """
    
    def __init__(self):
        # Setting time to pause between steps of stepper motor
        self.MOTOR_DELAY = 0.01 #sec

        # setup pins for rotation
        self.STEP_PIN_TURN = 2
        self.STEP_PIN_TILT = 14
        self.DIRECTION_PIN_TURN = 3
        self.DIRECTION_PIN_TILT = 15
        self.ENABLE_PIN_TURN = 4
        self.ENABLE_PIN_TILT = 17

        # starting head position
        self.turn_angle = 0 #deg
        self.tilt_angle = 0 #deg
        self.turn_steps = 0 # count of steps from neutral
        self.tilt_steps = 0 # count of steps from neutral

        return

    def connect(self, usb_port_address, bauderate, time_out = 1):
        """
        Sets up the initial serial communication connection
        """

        logging.info("Starts to connect components.")

        # connect components
        try:
            self.ser = serial.Serial(usb_port_address,
                                    bauderate, 
                                    timeout = time_out)
            self.connect_body = True # stores which components are connected.
            logging.info("Body component connected")
        except:
            self.connect_body = False
            logging.warning("Body component could not be connected.")
        
        try:
            # Head control via pin communicatoin
            GPIO.setmode(GPIO.BCM)
            ## motor 1: turning
            GPIO.setup(self.STEP_PIN_TURN, GPIO.OUT)
            GPIO.setup(self.DIRECTION_PIN_TURN, GPIO.OUT)
            GPIO.setup(self.ENABLE_PIN_TURN, GPIO.OUT)
            ## motor 2: tilting
            GPIO.setup(self.STEP_PIN_TILT, GPIO.OUT)
            GPIO.setup(self.DIRECTION_PIN_TILT, GPIO.OUT)
            GPIO.setup(self.ENABLE_PIN_TILT, GPIO.OUT)

            ## connecting to motors
            GPIO.output(self.ENABLE_PIN_TURN,GPIO.LOW)
            GPIO.output(self.ENABLE_PIN_TILT,GPIO.LOW)
            self.connect_head = True # stores which components are connected.
            logging.info("Head Component is connected.")
        except:
            self.connect_head = False
            logging.warning("Head Component could not be connected.")
        
        logging.info("Connected Head = {}, Body = {}".format(self.connect_head,
                                                            self.connect_body))

        return
    
    def disconnect(self):
        """
        Disconnects the serial communication.
        """
        if self.connect_body:
            self.ser.close()

        if self.connect_head:
            GPIO.cleanup()

        logging.info("Disconected components successfully.")
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
        """
        if self.connect_body is False:
            logging.warning("Method move(): Cannot execute command. Body disconneted.")
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
        read = None
        while(read != b'next\n'):
            read = self.ser.readline()
            # print(read)
        
        # Sending new move string
        self.ser.write(str.encode(str(new_move)))
        logging.info("Move command sent: {}".format(new_move))


#--------------------------------------------------------------------
# Head Unit Control
#--------------------------------------------------------------------
    def resetHeadPosition(self):
        """
        Resets head to move to 0 deg turn and 0 deg tilt.
        --- Under development ---
        How do we know the position when we first run the 
        script?
        ----------------------------------------------
        """
        
        return 

    def __deg2step(self, degrees, CONVERSION_FACTOR):
        """
        Converts number of degrees to number of steps and step direction.
        --- Under development ---
        Add conversion factor: emperically determined.
        Check: Direction assumption
        ----------------------------------------------
        """
        # assuming that LOW goes left and HIGH turns right
        direction = GPIO.LOW if degrees <= 0 else GPIO.HIGH
        steps = round(CONVERSION_FACTOR*degrees,0) # rounding to next integer
        steps = abs(int(steps))                    # convert to positive int type
        return (direction,steps)


    def look(self, **kwargs):
        """ 
        --- Under development ---
        Add max degree safety feature
        -----------------------------
        Controls the field of vision by rotating head. 
        Takes arguments as follows:
        keyword:    [int] value
        tilt:       [deg]  -45 to 45 
        turn:       [deg] -160 to 160
        """
        if self.connect_head is False:
            logging.warning("Method look(): Cannot execute command. Head disconneted.")
            return
    
        steps_turn = 0
        direct_turn = None

        steps_tilt = 0
        direct_tilt = None

        for key in kwargs:
            if key == 'turn':
                if abs(kwargs[key]) > 160:
                    logging.warning(">>> Degrees of head rotation out of bounds.")
                    logging.warning(">>> Valid interval: [-160, 160]")
                    return
                degrees = kwargs[key] - self.turn_angle
                direct_turn, steps_turn = self.__deg2step(degrees, CONVERSION_FACTOR_TURN)
                self.turn_steps = self.turn_steps + (-1*steps_turn) \
                                if degrees < 0 else self.turn_steps + steps_turn
                self.turn_angle = self.turn_steps / CONVERSION_FACTOR_TURN
            elif key == 'tilt':
                if abs(kwargs[key]) > 45:
                    logging.warning("Degrees of head rotation out of bounds.")
                    logging.warning(">>> Valid interval: [-45, 45]")
                    return
                degrees = kwargs[key] - self.tilt_angle
                direct_tilt, steps_tilt = self.__deg2step(degrees, CONVERSION_FACTOR_TILT)
                self.tilt_steps = self.tilt_steps + (-1*steps_tilt) \
                                if degrees < 0 else self.tilt_steps + steps_tilt
                self.tilt_angle = self.tilt_steps / CONVERSION_FACTOR_TILT   
            else:
                logging.warning("Invalid command input to look().")

        # Choosing max steps value
        steps = steps_turn if steps_turn > steps_tilt else steps_tilt

        # Setting direction
        GPIO.output(self.DIRECTION_PIN_TURN,direct_turn)
        GPIO.output(self.DIRECTION_PIN_TILT,direct_tilt)

        logging.info("Look command sent: turn={}, tilt={}".format(direct_turn,direct_tilt))

        # Sending signal to motors
        for i in range(steps):
            if i < steps_turn:
                GPIO.output(self.STEP_PIN_TURN,GPIO.LOW)
            if i < steps_tilt:
                GPIO.output(self.STEP_PIN_TILT,GPIO.LOW)
            time.sleep(self.MOTOR_DELAY)
            if i < steps_turn:
                GPIO.output(self.STEP_PIN_TURN,GPIO.HIGH)
            if i < steps_tilt:
                GPIO.output(self.STEP_PIN_TILT,GPIO.HIGH)
            time.sleep(self.MOTOR_DELAY)
        logging.info("Head arrived at target position.")
        return


    
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
    obj = Robot()
    obj.connect(PORT,BAUDERATE,TIMEOUT)
    try:
        print(" >>> START TEST SEQUENCE <<<")
        print(">>> WALK & LOOK SLIGHTLY RIGHT, UP <<<")
        obj.look(turn=90,tilt=35)
        for _ in range(30):
            obj.move(forward=0.3)
            time.sleep(0.1)
        print(">>> HIGH WALK & LOOK FROM INITIAL POSITION <<<")
        obj.look(turn=0,tilt=0)
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
