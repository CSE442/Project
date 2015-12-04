#!/usr/bin/env python2
#
# file:    gameTracker.py
# authors: Jacob Rutowski
# refrence: Code sourced from http://www.youtube.com/watch?v=jihxqg3kr-g
# purpose: Provides setup for camera and colored blog tracking

# orange: if R>G>B & (R/2)


import time
import sys
import cv2
import numpy as np
import SimpleCV

CAMERA_INDEX = 0

COLOR_BINARIZATION_THRESHOLD = 30  # change this value according to
                                   # segmented mode

DOT_DIMENSION = 30


DOTS = [#{'name': 'carton',
          #'color': (20.0, 19.0, 16.0)},
         #{'name': 'pink',
           #'color': (150, 45, 80)},
         # {'name': 'orange',
         #  'color': (163.0, 97.0, 59.0)},
         # {'name': 'yellow',
         #  'color': (160.0, 126.0, 8.0)}
         {'name': 'green',
          'color': (0,255,0)}
          ]
         
        

def distance_from_color(image, color):
	''' SimpleCV.Image, tuple -> int
		tuple: (b,g,r)
		'''
	matrix = (image.getNumpy()[:, :, [2,1,0]]-color)**2
	width, height = image.size()
	return matrix.sum() ** 0.5 / (width * height)

def main():

	print("This is where we print useful stuff in the terminal")
	tracking_cam = SimpleCV.Camera(camera_index=CAMERA_INDEX)
	display = False
	if len(sys.argv) > 1:
		display = sys.argv[1]

	#waits for some time to allow camera to initialize
	time.sleep(1)
	background = tracking_cam.getImage()

	print("Beggining tracking")

	while True:
		image = tracking_cam.getImage()
		##between these comments is us playing with masking colors to pass

		lower_green = np.array([0,160,0])
		upper_green = np.array([130,255,130])

		##lower_pink = np.array([148,40,75])
		##upper_pink = np.array([155,48,83])

		##pink_mask = cv2.inRange(image.getNumpy(), lower_pink, upper_pink)
   		green_mask = cv2.inRange(image.getNumpy(), lower_green, upper_green)

   		##new_mask = (pink_mask+green_mask)
		##
		##between these comments is us playing with masking colors to pass

		dist = ((image - background) + (background - image)).dilate(10)
		segmented = dist.binarize(COLOR_BINARIZATION_THRESHOLD).invert()
		blobs = segmented.findBlobs(minsize=DOT_DIMENSION ** 2)
		if blobs:
			points = []
			for blob in blobs:
				points.append((blob.x, blob.y))
				detected = image.crop(blob.x, blob.y, DOT_DIMENSION, DOT_DIMENSION, centered=True)
				#color distances from detected
				distances=[distance_from_color(detected, d['color']) for d in DOTS]
				chosen_dot = DOTS[np.argmin(distances)]['name']
				print(blob.x, blob.y, chosen_dot)

		if display:
			to_show = locals()[display]
			if blobs:
				to_show.drawPoints(points)
			to_show.show()
			#playing with masking


		else:
			time.sleep(0.1)

if __name__=='__main__':
	main()


