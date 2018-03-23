import serial

class Robot(object):
    """
    Object to control Minitaur Robot that reacts to 8 byte integer 
    command.
    """
    
    def __init__(self):
        pass

    def connect(self, usb_port_address, bauderate, time_out = 1):
        """
        Sets up the initial serial communication connection
        """
        self.ser = serial.Serial(usb_port_address,
                                bauderate, 
                                timeout = time_out)
    
    def disconnect(self):
        """
        Disconnects the serial communication.
        """
        self.ser.close()

    def __convertToCommand(self, float_in):
        """
        Takes in command in float form and encodes command as two digit string.
        """
        int_in = int(float_in * 10)
        first_digit = 0 if int_in < 0 else 1    #encodes negative
        second_digit = abs(int_in)              #only consider magnitude
        return (first_digit, second_digit)

    def command(self, **kwargs):
        """
        Controls main body translation.
        Converts command input to 8 byte integer.
        Takes arguments as follows:
            behavior    [int]                      0 to 9,
            forward     [m/s]                   -0.9 to 0.9,
            turn        [rad/s]                 -0.9 to 0.9,
            height      [% relative to normal]  -0.9 to 0.9
        """
        new_command = list("90000000")

        for key in kwargs:
            if key == 'forward':
                new_command[2:4] = self.__convertToCommand(kwargs[key])
            elif key == 'turn':
                new_command[4:6] = self.__convertToCommand(kwargs[key])
            elif key == 'height':
                new_command[6:8] = self.__convertToCommand(kwargs[key])
            elif key == 'behavior':
                new_command[1] = int(kwargs[key])

        new_command = map(str,new_command) # converting int to char
        new_command = ''.join(new_command) # joining char to str

        # Waiting for Signal that Minitaur is ready to receive command input
        read = None
        while(read != b'next\n'):
            read = self.ser.readline()
            print(read)
        
        # Sending new command string
        self.ser.write(str.encode(str(new_command)))
    
if __name__ == '__main__':
    """
    For example code see below.
    
    Test routine: 
     - walk forward 3sec, 
     - walk at higher standing height normal height 2sec, 
     - sit 2 sec,
     - return to starting position
    """
    import time # for consistency

    # different for every computer
    PORT = '/dev/tty.usbserial-DN01QALN' 
    BAUDERATE = 115200
    TIMEOUT = 1
    obj = Robot()
    obj.connect(PORT,BAUDERATE,TIMEOUT)
    print(" >>> START TEST SEQUENCE <<<")
    print(">>> WALK <<<")
    for _ in range(30):
        obj.command(forward=0.3)
        time.sleep(0.1)
    print(">>> HIGH WALK <<<")
    for _ in range(20):
        obj.command(forward=0.2,height=0.3)
        time.sleep(0.1)
    print(">>> SIT <<<")
    for _ in range (20):
        obj.command(height = -.9)
        time.sleep(0.1)
    print(">>> STAND <<<")
    for _ in range (20):
        obj.command()
        time.sleep(0.1)
    
    obj.disconnect()
    print(">>> TEST COMPLETE <<<")

