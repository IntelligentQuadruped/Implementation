# IQ
PORT = '/dev/ttyUSB0' #USB-port address
BAUDERATE = 115200
HEAD_CONNECTED = True
N_AVERAGE_DIRECTIONS = 3 # Number of averaged direction commands
Z_SCORE_THRESHOLD = 3
DEBUG = False
INITIAL_DELAY = 1#sec


# Camera
MAX_DEPTH = 20.0
FRAMES_AVRGD = 2
HEIGHT_RATIO = 0.5
SUB_SAMPLE = .5
SAVE_FRAME = False
SAVE_FRAME_INTERVAL = 2.0 # every [value] seconds
OUTPUT_DIR = "./trials"

# Navigation
MAX_DIST = 1.2 #meter
BARRIER_HEIGHT = 0 #relative to frame height
PERC_SAMPLES = 0.01
MIN_AGS_SIGMA = .4
MIN_AGS_H = 25
#Options are: 'upper','middle_upper','middle','middle_lower','lower'
NAV_FOCUS = 'middle_upper' #Considers the middle of the input frame. 
#Options are: 'rbf','voronoi','ags_only'
ALGORITHM = 'ags_only'

# Robot
FORWARD = 0.2 # Walking speed in m/s
MAX_TURN = 0.7 # Turning rate
MIN_TURN = 0.1 # Turning rate
WALKING_HGHT = -0.1 # Deviation from neutral walking height




