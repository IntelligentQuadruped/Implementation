# IQ
PORT = '/dev/ttyUSB0' #USB-port address
BAUDERATE = 115200
HEAD_CONNECTED = True
N_AVERAGE_DIRECTIONS = 3 # Number of averaged direction commands
Z_SCORE_THRESHOLD = 3
DEBUG = False
INITIAL_DELAY = 15#sec


# Camera
MAX_DEPTH = 4.0 # 4.0 meter for indoors / something larger for outdoors
FRAMES_AVRGD = 2
HEIGHT_RATIO = 0.5
SUB_SAMPLE = .5
SAVE_FRAME = False
SAVE_FRAME_INTERVAL = .5 # every [value] seconds
OUTPUT_DIR = "./trials"

# Navigation
MAX_DIST = 1.4 #meter
BARRIER_HEIGHT = 0.3 #relative to frame height
RBF_SAMPLING = 0.01 #What is this supposed to do?
PERC_SAMPLES = 0.01
MIN_AGS_SIGMA = .2
MIN_AGS_H = 25
#Options are: 'upper','middle_upper','middle','middle_lower','lower'
NAV_FOCUS = 'middle_upper' #Considers the middle of the input frame. 
#Options are: 'rbf','voronoi','ags_only'
ALGORITHM = 'rbf'

# Robot
FORWARD = 0.3 # Walking speed in m/s
MAX_TURN = 0.7 # Turning rate
MIN_TURN = 0.1 # Turning rate
WALKING_HGHT = 0.0




