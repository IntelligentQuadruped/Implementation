# IQ
PORT = '/dev/ttyUSB0' #USB-port address
BAUDERATE = 115200
N_AVERAGE_DIRECTIONS = 5 # Number of averaged direction commands
INITIAL_DELAY = 1#sec
Z_SCORE_THRESHOLD = 3
DEBUG = True

# Camera
FRAMES_AVRGD = 2
HEIGHT_RATIO = 0.5
SUB_SAMPLE = .5
SAVE_FRAME = False
SAVE_FRAME_INTERVAL = 2.0 # every [value] seconds
OUTPUT_DIR = "./trials"

# Navigation
MAX_DIST = 1. #meter
BARRIER_HEIGHT = 0.5 #relative to frame height
RBF_SAMPLING = 0.01 #What is this supposed to do?
PERC_SAMPLES = 0.01
MIN_AGS_SIGMA = .5
MIN_AGS_H = 15
#Options are: 'upper','middle_upper','middle','middle_lower','lower'
NAV_FOCUS = 'middle_lower' #Considers the middle of the input frame. 
#Options are: 'rbf','voronoi','ags_only'
ALGORITHM = 'ags_only'

# Robot
FORWARD = 0.2 # Walking speed in m/s
MAX_TURN = 0.5 # Turning rate
MIN_TURN = 0.1 # Turning rate




