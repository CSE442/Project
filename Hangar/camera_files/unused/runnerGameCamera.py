#runnerGameCamera.py
import gameCamera
import cv2


feed = gameCamera.Camera()

while(1):
	#feed.get_Image()

	#feed.get_HSV_Image()

	feed.displayFrame()
	#print feed.getColorPositions()
	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		cv2.imwrite("finalFrame.png", feed.get_Image())
		cv2.imwrite("finalFrameHSV.png", feed.get_HSV_Image())
		
		break