import numpy as np 
import cv2



def saveAsJPG(bgr_array,d_array,index = 0):
    '''
    Saves numpy arrays as jpg images that can be used for NN training.
    '''
    cv2.imwrite('./bgr%d.jpg'%(index),bgr_array)
    cv2.imwrite('./dep%d.jpg'%(index),d_array)

class TakeVideo(object):
    '''
    Creates a video from cv2 image inputs (numpy array type).
    '''

    def __init__(self, video_name, width, height, ending = 'mp4v'):
        ''' 
        Initializes new video file.
        '''
        self.height = height
        self.width = width
        self.fourcc = cv2.VideoWriter_fourcc(*ending) # Be sure to use lower case
        self.out = cv2.VideoWriter(video_name, self.fourcc, 20.0, (width, height))
        print("New video created: %s.%s"%(video_name,ending))
    
    def addFrame(self, frame):
        '''
        Adds a frame to video file
        '''
        try:
            h, w, _ = frame.shape
        except ValueError:
            print("Frame has fewer than three channels")
        else:
            h, w = frame.shape # in black and white case

        if h == self.height or w == self.width:
            self.out.write(frame)
        else:
            print("ERROR: Dimensions don't agree. \
            Video (%d,%d) Frame (%d,%d)"%(self.height,self.width,h,w))

    def saveVideo(self):
        '''
        Ends recording of video file and saves the video
        '''
        self.out.release()
