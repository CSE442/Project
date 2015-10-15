import cv2
import numpy as np
#ref
#http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html

cv2.namedWindow("testWindow", cv2.CV_WINDOW_AUTOSIZE)

capturePort = 0
camera = cv2.VideoCapture(capturePort)


def __del__():
    self.video.release()
    
def get_image():
        retval, im = camera.read()
        return im

DEFAULT_FRAME_WIDTH =1280
DEFAULT_FRAME_HEIGHT=720

FRAME_HEIGHT=DEFAULT_FRAME_HEIGHT
FRAME_WIDTH=DEFAULT_FRAME_WIDTH

MIN_OBJECT_AREA = 20*20
MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH

#def repeat():
print("Attempting to grab video frames")
#	testframe = cv2.QueryFrame(capture)
while True:
	#testFrame = camera.video.read()
	#cv2.ShowImage("testWindow", testframe)
	_, frame = camera.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	

	cv2.imshow('frame',frame)
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break
cv2.destroyAllWindows()