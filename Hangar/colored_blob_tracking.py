#!/usr/bin/env python2
#
# file:    colored_Blob_tracking.py
# authors: Aaron Preston, Jacob Rutowski, Lois Leport
# purpose: Provide a more organized and concise 
#	implementation of the blob color tracking from 
#	colorOptimization_2.py
# 

##########Settings

#The web cam designated number for open cv to mount, usualy "zero" 0 or "one" 1.
camera_port=0
#The Dictionary of colors which are applicable
colors_dict = {
	"blue"={
		#HSV color values
		"upper_bound"=(0,0,0)
		"lower_bound"=(0,0,0)
		"exists"=False
	}
	"red"={
		#HSV color values
		"upper_bound"=(0,0,0)
		"lower_bound"=(0,0,0)
		"exists"=False
	}
	"green"={
		#HSV color values
		"upper_bound"=(0,0,0)
		"lower_bound"=(0,0,0)
		"exists"=False
	}	
}

#########Functions
def isColor(R,G,B,color_object):
	#convert pixel from BGR to HSV
	#check if in range and Return True or False

	#Example:
	# Mat src=imread("image.jpg");
	# Mat HSV;
	# Mat threshold;

	# cvtColor(src,HSV,CV_BGR2HSV);
	# inRange(HSV,Scalar(106,60,90),Scalar(124,255,255),threshold);
	# imshow("thr",threshold);   

def
