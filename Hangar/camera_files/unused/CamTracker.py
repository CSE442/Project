import cv2
import numpy as np
#ref
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

cv2.namedWindow("testWindow", cv2.CV_WINDOW_AUTOSIZE)

capturePort = 0
camera = cv2.VideoCapture(capturePort)


def __del__():
    self.video.release()
    
#possbily useful method to grab a single frame
#from camera and save to file.
def get_image():
        retval, im = camera.read()
        return im


DEFAULT_FRAME_WIDTH =1280
DEFAULT_FRAME_HEIGHT=720

FRAME_HEIGHT=DEFAULT_FRAME_HEIGHT
FRAME_WIDTH=DEFAULT_FRAME_WIDTH

MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH

print("Attempting to grab video frames")

while True:
	
    #Reads a frame from the camera and stores 
	_, frame = camera.read()

	#converts frame from BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	
	#feeds the image frame to testWindow for 
	#debuging/tesing display
	cv2.imshow('testWindow',frame)

	#The following allows the running while 
	#loop to be broken by pressing ESC closing 
	#the program
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		cv2.imwrite("finalFrame.png", frame)
		break
cv2.destroyAllWindows()