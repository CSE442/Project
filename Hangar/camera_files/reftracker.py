import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([100,100,50])
    upper_blue = np.array([130,255,255])

    lower_green = np.array([65,50,75])
    upper_green = np.array([95,255,125])

    lower_red = np.array([0,70,70])
    upper_red = np.array([0,130,130])

    # Threshold the HSV image to get only correct colors
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    blue_res = cv2.bitwise_and(frame,frame, mask= blue_mask)
    green_res = cv2.bitwise_and(frame,frame, mask= green_mask)
    red_res = cv2.bitwise_and(frame,frame, mask= red_mask) 


    cv2.imshow('frame',frame)
    cv2.imshow('blue_mask',blue_mask)
    cv2.imshow('blue_res',blue_res)
    cv2.imshow('green_mask',green_mask)
    cv2.imshow('green_res',green_res)
    cv2.imshow('red_mask',red_mask)
    cv2.imshow('red_res',red_res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()