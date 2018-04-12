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
        self.forward = 0.0
        self.turn = 0.0
        self.height = 0.0
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
    def __rampUp(self,key, value):
        """
        Ramps up command inputs steadily to prevent erradic movements
        """
        cmd = getattr(self,key)
        # avoid float point exceptions
        cmd = round(cmd,1)
        value = round(value,1)
        if  cmd < value:
            cmd = cmd + 0.1
        elif cmd > value:
            cmd = cmd - 0.1
        else:
            pass
        setattr(self,key,cmd)
        return cmd

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
        if not self.connect_body:
            logging.warning("robot.py: Method move(): Cannot execute command. Body disconneted.")
            return

        new_move = list("90000000")

        for key in kwargs:
            if key == 'forward':
                fwd = self.__rampUp(key,kwargs[key])
                new_move[2:4] = self.__convertToMove(fwd)
            elif key == 'turn':
                trn = self.__rampUp(key,kwargs[key])
                new_move[4:6] = self.__convertToMove(trn)
            elif key == 'height':
                hght = self.__rampUp(key,kwargs[key])
                new_move[6:8] = self.__convertToMove(hght)
            elif key == 'behavior':
                new_move[1] = int(kwargs[key])

        new_move = map(str,new_move) # converting int to char
        new_move = ''.join(new_move) # joining char to str

        # Waiting for Signal that Minitaur is ready to receive move input
        read = None # Stores messages from Minitaur
        received = False # True iff the correct message was received
        while(read != b'next\n'):
            # print(read)
            read = self.ser.readline()
            
            try:
                # Logs warning when battery voltage is too low or motor temp to high
                if 'WARNING' in str(read,"utf-8"):
                    warning_str = str(read,"utf-8")[8:len(str(read,"utf-8"))]
                    if 'voltage' in str(read,"utf-8"):
                        logging.warning("robot.py: Battery Voltage too low")
                        logging.info("robot.py: " + warning_str)
                    if 'temperature' in str(read,"utf-8"):
                        # Won't currently work because .getTemperature() 
                        # isn't implemented on Minitaur SDK
                        logging.warning("robot.py: " + warning_str)
                # converts bites to unicode str
                if str(self.current_command) in str(read,"utf-8"):
                    received = True

            except UnicodeDecodeError:
                logging.warning("robot.py: Communication couldn't be decoded")

        # Sending new move string
        self.ser.write(str.encode(str(new_move)))

        # Through warning if move command wasn't correctly received by Minitaur
        if not received:
            logging.warning("robot.py: Last Move command {} was not received by Minitaur."\
                            .format(self.current_command))

        # Update current move command and log command
        if self.current_command != new_move:
            self.current_command = new_move
            logging.info("robot.py: Move command sent: {}".format(new_move))
        
        return received


    def testMove(self, **kwargs):
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
                fwd = self.__rampUp(key,kwargs[key])
                new_move[2:4] = self.__convertToMove(fwd)
            elif key == 'turn':
                trn = self.__rampUp(key,kwargs[key])
                new_move[4:6] = self.__convertToMove(trn)
            elif key == 'height':
                hght = self.__rampUp(key,kwargs[key])
                new_move[6:8] = self.__convertToMove(hght)
            elif key == 'behavior':
                new_move[1] = int(kwargs[key])
            print(key)

        new_move = map(str,new_move) # converting int to char
        new_move = ''.join(new_move) # joining char to str

        print("Move command sent: {}".format(new_move))


    
if __name__ == '__main__':
    """
    Offline Test routine: 
     -  walk forward 3sec and rotate head slightly up and right, 
     -  walk at higher standing height normal height 2sec 
            and turn head to starting position, 
     -  sit 2 sec,
     -  return to starting position
    """
    obj = Robot()
    try:
        print(" >>> START TEST SEQUENCE <<<")
        print(">>> Stand <<<")
        for _ in range(30):
            obj.testMove()
            time.sleep(0.1)
        print(">>> WALK <<<")
        for _ in range(30):
            obj.testMove(forward=0.3,height = .1)
            time.sleep(0.1)
        print(">>> Turn right<<<")
        for _ in range(20):
            obj.testMove(forward=0.1,turn =.6, height=.1)
            time.sleep(0.1)
        print(">>> Turn left <<<")
        for _ in range (20):
            obj.testMove(forward=0.1,turn=-.6,height=.1)
            time.sleep(0.1)
        print(">>> STAND <<<")
        for _ in range (20):
            obj.testMove()
            time.sleep(0.1)
        
    except KeyboardInterrupt:  
        print("Test ended prematurely and has been disconnected")