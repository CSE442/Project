#!/usr/bin/env python2
# encoding: utf-8

# file:gameCamera.py 
# desc:Camera API for MMATAA Game

import cv2
import numpy as np
from math import sqrt
import thread as thread

class Camera(object):
    """"Class to store camera atributes"""
    def  __init__(self):
        
        #sets up default values and book keeping vars
        DEFAULT_FRAME_WIDTH =1280
        DEFAULT_FRAME_HEIGHT=720

        FRAME_HEIGHT=DEFAULT_FRAME_HEIGHT
        FRAME_WIDTH=DEFAULT_FRAME_WIDTH

        MIN_OBJECT_AREA = 20*20
        MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH

        #selects which camera device to choose 
        #choose 0 
        # for either internal webcam or if only only a 
        # single camera attached 
        #choose 1
        # for using attached external camera if there is 
        # an existig webcam already etc. go up from there
        capturePort = 0
        self.camera = cv2.VideoCapture(capturePort)

        ##################################################
        #this section is for debugging durring development
        
        #creates a window for debug viewing
        cv2.namedWindow("testWindow", cv2.CV_WINDOW_AUTOSIZE)

        ##################################################


    def get_Image(self):
        """reads a single fram from the camera and returns it"""
        retval, im = self.camera.read()
        return im

    def get_HSV_Image(self):
        """reads a single fram from the camera and returns it"""
        retval, im = self.camera.read()
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        return hsv

    def displayFrame(self):
        cv2.imshow('testWindow',self.get_Image())
        pass

    def getColorPositions(self):
        """Returns the current coordinates of the cars by color"""
        workingFrame = self.get_HSV_Image()

        colorPositions = {
            "blue_x":0,
            "blue_y":0,
            "blue_z":0,

            "green_x":0,
            "green_y":0,
            "green_z":0,
            
            "red_x":0,
            "red_y":0,
            "red_z":0
        }

        return colorPositions