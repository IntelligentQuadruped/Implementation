
import serial
import getch

forward = True

# Config Constants (Later export to .json file)
PORT = '/dev/ttyUSB0' # dmesg | grep tty
BAUDERATE = 115200
TIMEOUT = 2 # set to 1 for normal use, 2 for debugging


ser = serial.Serial(PORT,BAUDERATE,timeout = TIMEOUT)



while(True):

    msg = None
    char = getch.getch()
    
    if char == 'w':
        forward = True
        msg = 90130000
    if char == 's':
        forward = False
        msg = 90030000
    if char == 'd':
        if forward:
            msg = 90131300
        else: msg = 90031300
    if char == 'a':
        if forward:
            msg = 90130300
        else: msg = 90030300
    if char == 'k':
        msg = 90000013
    if char == 'j':
        msg = 90000003

    # Add Error message for wrong command input
    string = str(msg)
    if(len(string) != 8): 
        assert len(string) != 8,'ERROR: Command string is not 8 bytes' 
        continue

    ser.write(str.encode(string))
    read = None
    while(read != b'next\n'):
        read = ser.readline()
        print(read)
